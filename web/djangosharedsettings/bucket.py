import os

'''
Make sure you add 'storages' to INSTALLED_APPS after 'django.contrib.admin'
'''

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = 'public-read'
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

'''
# Creating the bucket

If you are setting up a new instance from scratch you'll need to create a new
AWS S3 bucket. You'll also need an IAM policy that gives admin access to the
bucket for managing the media, and an IAM user with that policy, whose
credentials can be given to Django to actually read and write the files.

The policy needs to look like this, but with `missioncamden-dev-media` replaced
with your real bucket name:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::missioncamden-dev-media/*",
                "arn:aws:s3:::missioncamden-dev-media"
            ]
        }
    ]
}
```

The Bucket then needs this policy (again with `missioncamden-dev-media`
replaced with your real bucket name):

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::missioncamden-dev-media/*"
        }
    ]
}
```

and it needs this CORS config:

```
<CORSConfiguration>
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>Authorization</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```

The user you create doesn't need console access, only programmatic access, and
it only needs the IAM policy you created, no other permissions. When you create
it you'll need to save the credentials (you can't access them again later).
These credentials are then used to set these environment variables for Django
production:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME
```
'''

