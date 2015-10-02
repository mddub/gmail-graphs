import os
import sys
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parser
from dateutil.tz import tzlocal
from operator import itemgetter

import simplejson as json

# Assume the current system timezone is the same timezone as the log file names
# so we can assign a timezone to a timestamp like '2015-06-01_01_00_01.json'.
# (If this isn't true, use pytz.timezone instead.)
LOG_TIMEZONE = tzlocal()

# The amount of time after midnight on a date to use as the representative data
# point for that date. 25 hours means the log file closest to 1am on June 2 will
# be used as the data for June 1.
DATA_DELAY = timedelta(hours=25)

def date_to_datetime(d):
    return datetime.combine(d, datetime.min.time())

try:
    # This directory should contain files like '2015-06-01_01_00_01.json'
    LOG_DIR = sys.argv[1]
except IndexError:
    print "Usage: python {0} log_directory".format(sys.argv[0])
    sys.exit(1)

log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.json')]
timestamps_and_files = [
    (
        datetime.strptime(f, '%Y-%m-%d_%H.%M.%S.json'),
        os.path.join('messages', f)
    )
    for f in log_files
]
dates = sorted(set([d.date() for d, _ in timestamps_and_files]))

dates_and_representative_files = []
for d in dates:
    files_and_proximities = [(abs(ts - (datetime(d.year, d.month, d.day) + DATA_DELAY)), ts, f) for ts, f in timestamps_and_files]
    _, _, closest_file = sorted(files_and_proximities, key=itemgetter(0))[0]
    dates_and_representative_files.append((d, closest_file))

date_parser = parser()

date_to_ages = {}
for d, f in dates_and_representative_files:
    messages = json.loads(open(f).read())
    ages = []
    for i, m in enumerate(messages):
        msg_date = date_parser.parse(m['date'])
        if msg_date.tzinfo is None:
            # Occasionally, the date parser can't understand something like 'EDT'.
            # If you care, put a breakpoint here, see what it can't parse, special case it.
            # Otherwise, just assume local time.
            msg_date = msg_date.replace(tzinfo=LOG_TIMEZONE)
        # Compare dates, not datetimes. A message received at 3:15pm on Tuesday is 0 days old
        # from Tuesday 3:15pm until Tuesday 11:59pm, then 1 day old from Wednesday 0:00am until
        # Wednesday 11:59pm, etc.
        # (Caveat about datetime.replace: http://stackoverflow.com/questions/13994594/how-to-add-timezone-into-a-naive-datetime-instance-in-python)
        msg_age = date_to_datetime(d) - date_to_datetime(msg_date.astimezone(LOG_TIMEZONE).date())
        if msg_age.total_seconds() < 0:
            # if DATA_DELAY > 24 hours, we may see messages received on the following day
            continue
        ages.append(msg_age.days)
    date_to_ages[d.strftime('%Y-%m-%d')] = ages

print json.dumps(date_to_ages, sort_keys=True, indent='    ')
