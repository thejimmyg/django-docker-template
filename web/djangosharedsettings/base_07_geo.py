'''
If you had an existing database you'd need to re-run mugrations

```
alias manage.py='docker-compose -f `pwd`/docker-compose.yml run --rm web python3 manage.py'
manage.py migrate
```

You should be able to run every step in the GeoDjango tutorial here:

    https://docs.djangoproject.com/en/3.0/ref/contrib/gis/
'''

from .base_06_timezone import *


for app in [
    'django.contrib.admin',
    'django.contrib.gis',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
