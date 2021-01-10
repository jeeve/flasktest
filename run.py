#! /usr/bin/env python

from fbapp import app

"""
from flask import Flask
from gpsapp import app as gps_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound(), {
    '/meteo': meteo_app,
    '/gps': gps_app,
})
"""

if __name__ == "__main__":
    app.run(debug=True)

