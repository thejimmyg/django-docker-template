import os


EMAIL_BACKEND = 'djangosharedsettings.emailbackend.LoggingBackend'
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
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [host.strip() for host in os.environ['ALLOWED_HOSTS'].split(',')]
