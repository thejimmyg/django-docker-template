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

'''
# Essentially a username, replace XXX with your access key from the AWS web console
export AWS_ACCESS_KEY_ID=XXX
# Essentially a password, replace with your secret access key from the AWS web console
export AWS_SECRET_ACCESS_KEY=XXX
export AWS_DEFAULT_REGION=eu-west-1 
export AWS_DEFAULT_OUTPUT=json


To send email from SES you need to verify your email address or an entire
domain.

If you verify an entire domain, you can send emails from all that domain e.g.
user1@example.com, user2@example.com etc.

Instead, we'll just verify one identity:

```
export EMAIL_ADDRESS=user1@example.com
aws ses verify-email-identity --email-address "${EMAIL_ADDRESS}"
```

Now wait a few moments and check your email, click the link and follow the instructions to verify.

Create an IAM user to use for SMTP credentials:

```
aws iam create-user --user-name mysite-smtp
aws iam put-user-policy --user-name mysite-smtp --policy-name 'send-email' --policy-document '{ "Statement": [{"Effect":"Allow", "Action":"ses:SendRawEmail", "Resource":"*" }]}'
export CREDS=`aws iam create-access-key --user-name mysite-smtp --query "AccessKey.{AccessKeyId:AccessKeyId,SecretAccessKey:SecretAccessKey}" --output=text`
export SMTP_USERNAME=`echo "$CREDS" | awk '{print $1}'`
export SECRET_ACCESS_KEY_FOR_SMTP=`echo "$CREDS" | awk '{print $2}'`
export SMTP_PASSWORD=`(echo -en "\x02"; echo -n 'SendRawEmail' \
  | openssl dgst -sha256 -hmac $SECRET_ACCESS_KEY_FOR_SMTP -binary) \
  | openssl enc -base64`
echo "Username: $SMTP_USERNAME Password: $SMTP_PASSWORD SMTP host: email-smtp.$AWS_DEFAULT_REGION.amazonaws.com TLS: True Port: 587"
```

You can now send an email using SMTP.

**Caution: Make sure you use your *SMTP* credentials and not your AWS credentials, and make sure you use a secure TLS transport.**

'''
