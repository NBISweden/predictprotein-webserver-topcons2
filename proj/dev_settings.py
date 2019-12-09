"""
Django settings for proj project in development.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
try:
    from .shared_settings import *
except ImportError:
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5&!cq9#+(_=!ou=mco0=-qrmn6h66o(f)h$ho4+0vo1#d24xdy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATIC_ROOT = "%s/pred/static"%(BASE_DIR)

allowed_host_file = "%s/allowd_host_dev.txt"%(BASE_DIR)
computenodefile = "%s/pred/config/computenode.txt"%(BASE_DIR)
for f in [allowd_host_pro, computenodefile]:
    if os.path.exists(f):
        ALLOWED_HOSTS +=  myfunc.ReadIDList2(computenodefile,col=0)

# add also the host ip address
hostip = webcom.get_external_ip()
ALLOWED_HOSTS.append(hostip)

