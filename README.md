# gmail-graphs

Been using [gmail-logger] to collect data about your Gmail inbox, and want to generate graphs like those in my blog post, [Three Years of Logging My Inbox Count]? Perfect, because that's all this repo does.

Fair warning: a lot of this code is inelegant. Don't study it as an example of how to do Pandas/Matplotlib right. (If I were doing this again, I'd use D3.js. Customizing Matplotlib is hell.)

### Figure 3: Inbox count by age

![Figure 3: Inbox count by age](https://raw.githubusercontent.com/mddub/gmail-graphs/master/sample-output/figure-3.png)

See `calculate_email_ages_on_each_day.py` and the [Inbox count by age] notebook to graph the results.

### Other graphs

Coming soon.

[gmail-logger]: https://github.com/mddub/gmail-logger
[Three Years of Logging My Inbox Count]: http://warkmilson.com/2015/05/15/three-years-of-logging-my-inbox-count.html
[Inbox count by age]: http://nbviewer.ipython.org/github/mddub/gmail-graphs/blob/master/Inbox%20count%20by%20age.ipynb
