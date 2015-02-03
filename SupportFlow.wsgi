import os
import sys	
sys.path.append('/SupportFlow/SupportFlow/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'SupportFlow.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
