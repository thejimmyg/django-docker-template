import os

'''
Make sure you add 'storages' to INSTALLED_APPS after 'django.contrib.admin'
'''

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = os.environ['MEDIA_AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['MEDIA_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['MEDIA_AWS_SECRET_ACCESS_KEY']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = 'public-read'
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

'''
# Creating the bucket

# Essentially a username, replace XXX with your access key from the AWS web console
export AWS_ACCESS_KEY_ID=XXX
# Essentially a password, replace with your secret access key from the AWS web console
export AWS_SECRET_ACCESS_KEY=XXX
export AWS_DEFAULT_REGION=eu-west-1
export AWS_DEFAULT_OUTPUT=json

aws s3api create-bucket --bucket mysite-media --create-bucket-configuration LocationConstraint=$AWS_DEFAULT_REGION
aws s3api put-bucket-policy --bucket mysite-media --policy '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mysite-media/*"
        }
    ]
}'
aws s3api put-bucket-cors --bucket mysite-media --cors-configuration='{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET"],
      "AllowedHeaders": ["Authorization"],
      "MaxAgeSeconds": 3000
    }
  ]
}'

Create the user to be allowed to read and write to the bucket:

aws iam create-user --user-name mysite-media-user
export BUCKET_CREDS=`aws iam create-access-key --user-name mysite-media-user --query "AccessKey.{AccessKeyId:AccessKeyId,SecretAccessKey:SecretAccessKey}" --output=text`
export MEDIA_ACCESS_KEY=`echo "$BUCKET_CREDS" | awk '{print $1}'`
export MEDIA_SECRET_ACCESS_KEY=`echo "$BUCKET_CREDS" | awk '{print $2}'`
echo "Access key: $MEDIA_ACCESS_KEY Secret access key: $MEDIA_SECRET_ACCESS_KEY"
aws iam put-user-policy --user-name mysite-media-user --policy-name 'mysite-media-access' --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::mysite-media/*",
                "arn:aws:s3:::mysite-media"
            ]
        }
    ]
}'
'''
