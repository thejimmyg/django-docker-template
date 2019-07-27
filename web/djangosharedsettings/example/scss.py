'''
Add this to `requirements.txt`:

```
libsass
django-compressor
django-sass-processor
```

Add `libsass` to your Alpine `Dockerfile` `runbase` `apk add` command and `libsass-dev` to your Alpine `Dockerfile` `buildbase` `apk add` command.

Run `docker-compose build`.

Then copy this file into your settings as `base_07_sass.py` and add this to the top:

```
from .base_06_timezone import *
```

Then change `dev.py` and `production_01_bucket.py` to import from `.base_07_sass` instead of `.base_06_timezone`.

Write your SCSS in `mysite/css/mystyle.scss`.

Then use like this in your Django templates:

```
{% load sass_tags %}

<link href="{% sass_src 'mysite/css/mystyle.scss' %}" rel="stylesheet" type="text/css" />
```

Which renders as:

```
<link href="/static/mysite/css/mystyle.css" rel="stylesheet" type="text/css" />
```

If you don't want to expose the SASS/SCSS files in a production environment, change the `collectstatic` command in `run.sh.local` to:

```
manage.py collectstatic --ignore=*.scss
```

You can compile offline instead of dynamically with:

```
manage.py compilescss
```

See https://github.com/jrief/django-sass-processor for the full information.
'''

for finder in [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]:
    if finder not in STATICFILES_FINDERS:
        STATICFILES_FINDERS.append(finder)

for app in [
    'sass_processor',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

# Optionally, add a list of additional search paths, the SASS compiler may examine when using the @import "..."; statement in SASS/SCSS files:
#
# import os
# 
# SASS_PROCESSOR_INCLUDE_DIRS = [
#     os.path.join(PROJECT_PATH, 'extra-styles/scss'),
#     os.path.join(PROJECT_PATH, 'node_modules'),
# ]
# 
# Other settings you can set:
# 
# SASS_PROCESSOR_AUTO_INCLUDE = False
# SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.scss$'
# SASS_PRECISION = 8
# SASS_OUTPUT_STYLE = 'compact'
