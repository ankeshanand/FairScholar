"""
WSGI config for FairScholar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
os.environ['DJANGO_SETTINGS_MODULE'] = 'FairScholar.settings'
site.addsitedir('/home/ankesh/FairScholar/env/lib/python2.7/site-packages')
sys.path.append('/home/ankesh/FairScholar/')
# Add the app's directory to the PYTHONPATH
#sys.path.append('/home/ankesh/FairScholar/FairScholar')


# Activate your virtual env
activate_env=os.path.expanduser("/home/ankesh/FairScholar/env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

