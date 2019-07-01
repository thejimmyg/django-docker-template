# Email


To test email sending create a simple test script named `testsend.py` in the `web` directory:

```
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Subject here',
    'Here is the message.',
    settings.DEFAULT_FROM_EMAIL,
    [settings.ADMINS[0][1]],
    fail_silently=False,
)
```

They you can run it like this:

```
$ docker exec -it mysite_web_1 /usr/local/bin/python3 /code/testsend.py
```

You should see this in the logs:

```
Sending message 'Subject here' to recipients: ['james@example.com']
```

and you should receive the email.
