# Info

Here you can find some useful information to know when working with the project.

## Things we tried that did not work

**Pyrscope** simple example does not work, the fastapi one does but it only shows CPU information as documented. Although it mighte be interesting to see which functions take how much time to execute it is not necessary for now. We already have tracing which allows us to track functionally how long things take.
**Couchbase** we tried to run seperate database for testing but the ports can not be easily changed. We run the test database manually but configure it from the tests.
**Logging** the way local logging is implemented now, the stacktrace is not shown. It is shown in Loki.
