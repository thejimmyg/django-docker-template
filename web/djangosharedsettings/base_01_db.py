from .base import *
import os

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
if os.environ.get('ENABLE_GEO', 'false').strip().lower() == 'true':
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
