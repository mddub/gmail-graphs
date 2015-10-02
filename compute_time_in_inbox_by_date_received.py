import os
import sys
from collections import defaultdict
from datetime import datetime
from datetime import timedelta

import simplejson as json

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

timestamps_and_thread_ids = [
    (
        ts,
        set([m['thread_id'] for m in json.loads(open(f).read())])
    )
    for ts, f in timestamps_and_files
]

all_appearances = []
inbox_thread_to_date_of_appearance = {}

for (last_date, last_threads), (date, threads) in zip(timestamps_and_thread_ids[:-1], timestamps_and_thread_ids[1:]):
    for just_disappeared_thread in set(inbox_thread_to_date_of_appearance.keys()) - threads:
        # The thread disappeared from the inbox at some point between last_date
        # and date, so treat the average of last_date and date as the end of
        # this thread's tenure in the inbox. The higher the sample frequency,
        # the more accurate this method is.
        date_of_disappearance = last_date + (date - last_date) / 2
        all_appearances.append(
            (
                just_disappeared_thread,
                inbox_thread_to_date_of_appearance[just_disappeared_thread],
                date_of_disappearance - inbox_thread_to_date_of_appearance[just_disappeared_thread]
            )
        )
        del inbox_thread_to_date_of_appearance[just_disappeared_thread]

    for new_thread in threads - set(inbox_thread_to_date_of_appearance.keys()):
        # When an inbox sample contains a thread which was not seen in the
        # previous sample, consider that to be the start of this particular
        # period of the thread being in the inbox.
        #
        # It is possible for one thread to have multiple such periods. A thread
        # which appears in the inbox, is archived a day later, then reappears in
        # the inbox because of a response, then is archived again two days
        # later, will generate two entries, of two different lengths and on two
        # different dates.
        inbox_thread_to_date_of_appearance[new_thread] = date

tenures_by_date_received = defaultdict(list)
for thread_id, appearance_date, tenure_length in all_appearances:
    # Convert dates to strings and timedeltas to hours
    tenures_by_date_received[appearance_date.date().strftime("%Y-%m-%d")].append(
        round(tenure_length.total_seconds() / 3600.0, 2)
    )

sorted_tenures_by_date_received = dict(
    (key, sorted(values))
    for key, values in tenures_by_date_received.iteritems()
)

print json.dumps(sorted_tenures_by_date_received, sort_keys=True, indent='    ')
