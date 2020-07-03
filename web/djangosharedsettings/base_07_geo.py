'''
Geo support isn't enabled by default.

To enable it:

* Uncomment the geo lines in the `web/Dockerfile` and re-build
* Change the `db` to use PostGIS in your `docker-compose.yml`
* Set the `ENABLE_GEO` environment variable to `true` (this will set the database engine to `postgis` and enable the geo apps)

Note: PostGIS isn't supported easily on armv7 and the required packages aren't in Alpine 3.11 for arm which is why this isn't enabled by default.

You should be able to run every step in the GeoDjango tutorial here:

    https://docs.djangoproject.com/en/3.0/ref/contrib/gis/
'''

from .base_06_timezone import *
import os

if os.environ.get('ENABLE_GEO', 'false').strip().lower() == 'true':
    for app in [
        'django.contrib.admin',
        'django.contrib.gis',
    ]:
        if app not in INSTALLED_APPS:
            INSTALLED_APPS.append(app)
