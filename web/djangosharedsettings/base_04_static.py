from .base_03_logging import *



import os


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# Make sure your app is added to the INSTALLED_APPS setting of your site.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'


# Make sure you add 'whitenoise.middleware.WhiteNoiseMiddleware' after 'django.middleware.security.SecurityMiddleware' in MIDDLEWARE
MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')+1, 'whitenoise.middleware.WhiteNoiseMiddleware')
INSTALLED_APPS.insert(INSTALLED_APPS.index('django.contrib.admin'), 'storages')
STATIC_ROOT = os.path.join(ROOT_DIR, 'staticcache')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
