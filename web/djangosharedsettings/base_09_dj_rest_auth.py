'''

If you want to build a single page app using something like React you will want to be able
to make REST calls to Django AllAuth rather than using its templates and
views.

The `jg-rest-auth` module provides this functionality and it does it
on top of Django Rest Framework and Django AllAuth. The configuration set
up here will use JSON Web Tokens.

You can see the available API calls here:

https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html

Django AllAuth has a load of *social providers* which it supports via its templates and views.

Logging in with these social providers in a single page app is much trickier
(and potentially less secure) than using Django AllAuth's templates and views.
If you are writing a web app I'd personally recommend using Django AllAuth's
default social provider support based on web redirects. I'd use the single
page app for everything else, including registration, login, change email etc.

One situation where you can't use Django AllAuth's templates and views with web redirects for social providers is in a native app. In this situation you can use something like Expo's AuthSession and its auth proxy to get a short-lived *code* (a few seconds to a minute or two) entirely in the front end (with the help of a web browser popup) and then you can send this code to your server to verify on the backend with the social provider and then create a JWT that will give access to your app.

It is all a little complicated but there is an example of how to build the front end with Expo here:

* https://github.com/expo/examples/blob/001b693b1a20c2e34a62f35fc23a11fa84c48b56/with-facebook-auth/App.js

We'll use these ideas in our own example.

You can use `nvm` to install particular node versions, then install a recent lts version, then start an expo project:

```
$ nvm list
$ nvm use lts/dubnium
$ nvm i -g expo-cli
$ expo init myapp
$ cd myapp
```

You need to make some changes to the example:

* Add Web browser support
* Set a `DJANGO_PUBLIC_URL` to be used as the base URL for lots of the calls. This should be the public internet-facing URL for your running Django app, which in development is often a tunnel like ngrok
* Put your app's real Facebook ID at the top
* Add token exchange
* Use a WebView rather than user info

When you've made this changes you should end up with an `App.js` that is more like `web/djangosharedsettings/base_09_dj_rest_auth_App.js`

CAUTION: This approach sends all the tokens to an expo URL before it sends them back to the right place. You obviously shouldn't do this if you don't trust Expo, but getting this working without the proxy is even harder to get right.

When you are ready run:

```
expo start
```

Then click "Run on Andorid Emulator/Device" in the web interface that pops up. You'll need to install Android Studio and configure an emulator for this to work.

When you run this code, it will print out the `redirectUrl` that has been generated to the console. You can view the Android app console by clicking in the top right of the web interface to show the console panel.

You must also set this `redirectUrl` up as an allowed redirect URL in the Facebook web interface for the app. It will look something like this during development:

```
https://auth.expo.io/@<your_expo_username_or_anonymous>/<your_app_name>-<uid>
```

When testing locally in a browser you'll need a second ngrok proxy since localhost URLs aren't allowed in Facebook. This can point to http://localhost:19006 or similar.

Set this as your `FACEBOOK_REDIRECT_URL` setting in your settings so that it can be used in the code you write in `urls.py` later and make sure it is set in the Facebook dashboard too.

You then need to configure the integration. You can do this in the Django Admin by adding a new `Social application` under the `Social Accounts` app, or by loading your settings from a fixture.

To load your settings from a fixture, create a `social_application.json` file like this:

```
[
{
  "model": "socialaccount.socialapp",
  "pk": 1,
  "fields": {
    "provider": "facebook",
    "name": "fb",
    "client_id": "...",
    "secret": "...",
    "key": "",
    "sites": [
      1
    ]
  }
}
]
```

Then load it either using the alias you set up by following the README.md, or your own command:

```
mysite_noninteractive_manage.py loaddata social_application.json
```

To be able to exchange the Facebook *code* for your app's *JWT* you will still need to do two things:

* Implement the Facebook social provider end point
* Write some code in the example to exchange the code with the endpoint for a JWT and then make an authorised test call

You can implement a new endpoint like this in your `urls.py`:

```
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings

class FacebookLogin(SocialLoginView):
    client_class = OAuth2Client
    callback_url = settings.FACEBOOK_REDIRECT_URL
    adapter_class = FacebookOAuth2Adapter

urlpatterns += [
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
]
```

CAUTION: Make sure that it comes before the catch all Wagtail URL pattern, otherwise the request will go to Wagtail, and not this handler.

CAUTION: The `callback_url` here MUST match the `redirectUrl` in the front end and in the Facebook console.

CAUTION: Make sure the SITE_ID matches the actual domain of the site in your DJANGO_PUBLIC_URL, otherwise you might get errors that the social application does not exist.

Since the code you get from Facebook is only short-lived you have to quickly call your new endpoint to exchange it for your app's JWT.

Since the emulator or device you are testing on might not be on the same network as your development server you can set up a tunnel using ngrok to securely proxy requests from the public internet to your development app.

You run ngrok like this:

```
./ngrok http 80
```

and it will give you a secure tunnel URL something like this:

```
`https://<id>.ngrok.io/`
```

With the JWT access token issued by your app, you can now make authorised requests:

```
    let user = await fetch(
        'https://<id>.ngrok.io/dj-rest-auth/user/',
        {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + jwt,
            },
        },
    );
    let userJson = await user.json();
    console.log('REST auth call:', userJson);
```

For debugging you can always get a sample token from the Facebook app console and test it directly:

https://developers.facebook.com/tools/accesstoken/

Unfortunately the token you get is a test *access token*, not a test *code* so instead of doing this as the example above does:

```
curl -v -X POST -d "code=..." http://localhost:8000/dj-rest-auth/facebook/
```

You have to make an `access_token` call instead. The behaviour afterwards is the same though.

```
curl -v -X POST -d "access_token=..." http://localhost:8000/dj-rest-auth/facebook/
```

You can then test the JWT you get back:

```
curl -H 'Authorization: Bearer <jwt>' http://localhost:8000/dj-rest-auth/user/
```

With an invalid or missing JWT it should fail:

```
curl http://localhost:8000/dj-rest-auth/user/
curl -H 'Authorization: Bearer malformed' http://localhost:8000/dj-rest-auth/user/
```

The JWT support comes from `djangorestframework-simplejwt`. It is designed to have sensible defaults and it uses the `SECRET` setting by default which is set up by Django when you create a project (or when a new project is created in the case of the first run of the docker container in this case)

WARNING: This might be a red herring but the token exchange didn't seem to work if you have a custom `User` model. It said the Token has no attribute `.objects`. Of course, this might be because of something else.

See also:

Django:

* https://www.django-rest-framework.org/#installation
* https://www.django-rest-framework.org/api-guide/authentication/
* https://docs.djangoproject.com/en/3.0/intro/tutorial01/
* https://django-allauth.readthedocs.io/en/latest/configuration.html
* https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html

Inspecting JWTs:

* https://security.stackexchange.com/questions/124624/how-does-jti-prevent-a-jwt-from-being-replayed
* https://jwt.io

Facebook:

* https://developers.facebook.com/apps/<YOUR_FB_ID>/fb-login/settings/
* https://developers.facebook.com/tools/accesstoken/
* https://developers.facebook.com/tools/debug/accesstoken/

Expo:

* https://expo.io/learn
* https://docs.expo.io/versions/latest/sdk/auth-session/
* https://docs.expo.io/workflow/linking/?redirected
* https://docs.expo.io/guides/authentication/#facebook
* https://github.com/expo/examples/tree/master/with-facebook-auth
* https://github.com/expo/expo/blob/master/packages/expo-auth-session/build/AuthSession.js
'''


from .base_08_allauth import *


# https://github.com/jazzband/dj-rest-auth


# Should be as high as possible
# for app in [
#     'corsheaders',
# ]:
#     if app not in INSTALLED_APPS:
#         INSTALLED_APPS.insert(0, app)
# 
# CORS_ORIGIN_WHITELIST = [
#     "http://<your_site>:19006",
# ]

for app in [
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

for middleware in [
#    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]:
    if middleware not in MIDDLEWARE:
        MIDDLEWARE.append(middleware)

# print(INSTALLED_APPS)
# print(MIDDLEWARE)

# You need to set this:
# FACEBOOK_REDIRECT_URL = "http://localhost:19006"
# 'https://auth.expo.io/@anonymous/<app>-<id>

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'

if not 'REST_FRAMEWORK' in locals():
    REST_FRAMEWORK = {}

REST_FRAMEWORK.setdefault('DEFAULT_AUTHENTICATION_CLASSES', ())
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = list(REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])
for ac in [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
]:
    if ac not in REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']:
        REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(ac)

# For Facebook you might want this?
# ACCOUNT_EMAIL_VERIFICATION = 'none'

# See the dj-rest-auth section of urls.py

for app in [
    'django.contrib.sites', 'allauth', 'allauth.account', 'dj_rest_auth.registration'
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

if SITE_ID != 1:
    SITE_ID = 1

# /direct login for an email user:
# curl -v -X POST -d "username=admin&email=me@example.com&password=123123ab" http://localhost:8000/dj-rest-auth/login/
# After you've setup a Facebook REST endpoint
# /dj-rest-auth/facebook/
# curl -v -X POST -d "code=..." http://localhost:8000/dj-rest-auth/facebook/
