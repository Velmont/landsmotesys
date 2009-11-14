#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('/var/www/landsmotesys')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
