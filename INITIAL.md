# Initial Changes for a Django App

```
export PROJECT=mysite
```

## Update

`TIMEZONE` to `Europe/London` and language to `en_gb`.

## Settings

```
mkdir "$PROJECT/settings/"
mv "$PROJECT/settings.py" "$PROJECT/settings/base.py"
cat << EOF >> "$PROJECT/settings/base.py"


ADMINS = []
if os.environ.get('ADMINS'):
    ADMINS += [('admin', email.strip()) for email in os.environ['ADMINS'].split(',')]
if not len(ADMINS):
    raise Exception('Please specify at least one email in ADMINS')

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
if EMAIL_PORT:
    EMAIL_PORT = int(EMAIL_PORT)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# Let's have the default being True
EMAIL_USE_TLS = not str(os.environ.get('EMAIL_USE_TLS')).lower() == 'false'
# We use TLS, not SSL, so this isn't needed
EMAIL_USE_SSL = str(os.environ.get('EMAIL_USE_SSL')).lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', ADMINS[0])
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', ADMINS[0])
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [host.strip()
                      for host in os.environ['ALLOWED_HOSTS'].split(',')]

EOF
cat << EOF > "$PROJECT/settings/dev.py"
from .base import *

ALLOWED_HOSTS = ['*']
EOF
cat << EOF > "$PROJECT/settings/production.py"
from .base import *

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = [host.strip() for host in os.environ['ALLOWED_HOSTS'].split(',')]

EOF
```

## Database Settings

Edit `$PROJECT/settings/base.py` and change the `DATABASE` setting to point to `db`. Change this:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

To:

```
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
```

Emails:

```
EMAIL_BACKEND = '$PROJECT.emailbackend.LoggingBackend'
```

```
import django.core.mail.backends.smtp
import logging

logger = logging.getLogger(__name__)  # or you could enter a specific logger name
    
class LoggingBackend(django.core.mail.backends.smtp.EmailBackend):

    def send_messages(self, email_messages):
        try:
            for msg in email_messages:
                logger.error(u"Sending message '%s' to recipients: %s", msg.subject, msg.to)
        except:
            logger.exception("Problem logging recipients, ignoring")
   
        return super(LoggingBackend, self).send_messages(email_messages)
```

```
import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('ROOT_LOG_LEVEL', 'ERROR'),
        },
    },
}
```
