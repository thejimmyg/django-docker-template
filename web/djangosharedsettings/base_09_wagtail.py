"""
./manage.py startapp


and add it to INSTALLED_APPS

from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

urlpatterns = [
    ...
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^pages/', include(wagtail_urls)),
    ...
]


re_path(r'', include(wagtail_urls)),



from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

You might also want to add this management command for wiping the tables after a migrate so that you can loaddata.




from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Wipes the database tables associated with Wagtail using a CASCADE to other tables'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('''
              DELETE FROM wagtailcore_site CASCADE;
              DELETE FROM wagtailcore_grouppagepermission CASCADE;
              DELETE FROM wagtailcore_page CASCADE;
            ''')
            self.stdout.write(self.style.SUCCESS('Successfully wiped the tables'))
"""

from .base_08_allauth import *

# Based on http://docs.wagtail.io/en/v2.5.1/advanced_topics/settings.html
for middleware in [
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',

  'wagtail.core.middleware.SiteMiddleware',

  'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]:
    if middleware not in MIDDLEWARE:
        MIDDLEWARE.append(middleware)

for app in [
  'wagtail.contrib.forms',
  'wagtail.contrib.redirects',
  'wagtail.embeds',
  'wagtail.sites',
  'wagtail.users',
  'wagtail.snippets',
  'wagtail.documents',
  'wagtail.images',
  'wagtail.search',
  'wagtail.admin',
  'wagtail.core',

  'taggit',
  'modelcluster',

  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  'wagtailthemes',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

# Probably worth setting this to the same as Django's APPEND_SLASH
# https://docs.djangoproject.com/en/2.2/ref/settings/#append-slash
WAGTAIL_APPEND_SLASH = APPEND_SLASH = True

# To set up search follow: http://docs.wagtail.io/en/v2.5.1/advanced_topics/settings.html#search


# Based on http://docs.wagtail.io/en/v2.5.1/getting_started/integrating_into_django.html
for app in [
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    
    'modelcluster',
    'taggit',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

for middleware in [
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]:
    if middleware not in MIDDLEWARE:
        MIDDLEWARE.append(middleware)

# Media
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEDIA_URL = '/media/'

WAGTAIL_SITE_NAME = 'mysite'

# Wagtail menus
# https://wagtailmenus.readthedocs.io/en/stable/installation.html

for app in [
    'wagtail.contrib.modeladmin',  # Don't repeat if it's there already
    'wagtailmenus',
    'wagtailautocomplete',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

for cp in [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'wagtail.contrib.settings.context_processors.settings',
    'wagtailmenus.context_processors.wagtailmenus',
]:
    if cp not in TEMPLATES[0]['OPTIONS']['context_processors']:
        TEMPLATES[0]['OPTIONS']['context_processors'].append(cp)

#  manage.py migrate wagtailmenus





# Wagtail themes:

for app in [
    'wagtail.contrib.settings',
    'wagtailthemes',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
for middleware in [
    'wagtailthemes.middleware.ThemeMiddleware',
]:
    if middleware not in MIDDLEWARE:
        MIDDLEWARE.append(middleware)
if 'loaders' not in TEMPLATES[0]['OPTIONS']:
    TEMPLATES[0]['OPTIONS']['loaders'] = []

for loader in [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]:
    if loader not in TEMPLATES[0]['OPTIONS']['loaders']:
        TEMPLATES[0]['OPTIONS']['loaders'].append(loader)
TEMPLATES[0]['OPTIONS']['loaders'].insert(0, 'wagtailthemes.loaders.ThemeLoader')


# Have to make sure APP_DIRS isn't present.
# Remove 'APP_DIRS': True at this position
del TEMPLATES[0]['APP_DIRS']


WAGTAIL_THEME_PATH = 'themes'
WAGTAIL_THEMES = [
    ('default', 'Default'),
    ('none', 'None'),
]
