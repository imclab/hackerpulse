#!/usr/bin/env python

from google.appengine.ext.webapp import util
from hackerpulse import app

if __name__ == '__main__':
	util.run_wsgi_app(app)
