# gmail-graphs

Been using [gmail-logger] to collect data about your Gmail inbox, and want to generate graphs like those in my blog post, [Three Years of Logging My Inbox Count]? Perfect, because that's all this repo does.

Fair warning: a lot of this code is inelegant. Don't study it as an example of how to do Pandas/Matplotlib right.

### Quick start

Make sure you have `ipython`, `pip`, and `virtualenv` installed.

```
git clone https://github.com/mddub/gmail-graphs
cd gmail-graphs
virtualenv venv && . venv/bin/activate
pip install -r requirements.txt
ipython notebook --pylab inline
```

### Figures 1 & 2: Inbox count over time

![Figure 2: Inbox count over time](https://raw.githubusercontent.com/mddub/gmail-graphs/master/sample-output/figure-2.png)

Follow the [Inbox count over time] IPython Notebook.

### Figure 3: Inbox count by age

![Figure 3: Inbox count by age](https://raw.githubusercontent.com/mddub/gmail-graphs/master/sample-output/figure-3.png)

See `compute_ages_on_each_day.py` and the [Inbox count by age] IPython Notebook to graph the results.

### Figure 4: Length of time a message spends in inbox, by date of arrival

![Figure 4: Length of time a message spends in inbox, by date of arrival](https://raw.githubusercontent.com/mddub/gmail-graphs/master/sample-output/figure-4.png)

See `compute_time_in_inbox_by_date_received.py` and the [Length of time a message spends in inbox] IPython Notebook to graph the results.

### Issues / enhancements

I've tried my best to generalize this code to run against anyone's [gmail-logger] data, but I can't foresee how well others' data will play with it. If you run into issues, please [file an issue]. If you have enhancements, pull requests are welcome.

[gmail-logger]: https://github.com/mddub/gmail-logger
[Three Years of Logging My Inbox Count]: http://warkmilson.com/2015/05/15/three-years-of-logging-my-inbox-count.html
[Inbox count by age]: http://nbviewer.ipython.org/github/mddub/gmail-graphs/blob/master/Inbox%20count%20by%20age.ipynb
[Inbox count over time]: http://nbviewer.ipython.org/github/mddub/gmail-graphs/blob/master/Inbox%20count%20over%20time.ipynb
[Length of time a message spends in inbox]: http://nbviewer.ipython.org/github/mddub/gmail-graphs/blob/master/Length%20of%20time%20a%20message%20spends%20in%20inbox.ipynb
[file an issue]: https://github.com/mddub/gmail-graphs/issues
