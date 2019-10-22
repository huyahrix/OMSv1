# Flask access log – write requests to file

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

you may be confused because adding a handler to Flask’s app.logger doesn’t catch the output you see in the console like:

127.0.0.1 - - [19/Apr/2014 18:51:26] "GET / HTTP/1.1" 200 -
This is because app.logger is for Flask and that output comes from the underlying WSGI module, Werkzeug.

To access Werkzeug’s logger we must call logging.getLogger() and give it the name Werkzeug uses. This allows us to log requests to an access log using the following:

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)

- Also add the handler to Flask's logger for cases
where Werkzeug isn't used as the underlying WSGI server.
app.logger.addHandler(handler)
- You can of course add your own formatting and other handlers.
- https://docstrings.wordpress.com/2014/04/19/flask-access-log-write-requests-to-file/

# Loglevel
    The granularity of Error log outputs.

    Valid level names are:

    debug
    info
    warning
    error
    critical