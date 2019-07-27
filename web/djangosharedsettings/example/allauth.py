'''
Install:

```
pip install django-allauth
```

or add `django-allauth` to `requirements.txt`.

Then you need to change the import chain in `dev.py` and `production.py` so that they import the settings from this modules, and so that this module imports from whatever the ones were before.

For adding a social account for Google visit  https://developers.google.com/identity/sign-in/web/sign-in?refresh=1 The callback you need for testing is: http://127.0.0.1:8000/accounts/google/login/callback/

urls.py - the configuration below overrides some of the other login screens:

```
from django.contrib import admin
from django.urls import include, path
from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from django.views.generic.base import RedirectView


app_name = 'teratree'
urlpatterns = [
    # Instead, follow this pattern
    path('meeting/', include('meeting.urls')),
    path('data/', include('data.urls')),
    path('experiment/', include('experiment.urls')),
    # This is how wagtail recommends it is done, don't copy this
    re_path(r'^documents/', include(wagtaildocs_urls)),
    path('cms/login/', RedirectView.as_view(url='/accounts/login', query_string=True, permanent=False), name='index'),
    path('_util/login/', RedirectView.as_view(url='/accounts/login', query_string=True, permanent=False), name='index'),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    path('admin/login/', RedirectView.as_view(url='/accounts/login', query_string=True, permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # Put this after accounts above to use the AllAuth URLs by default
    re_path(r'^', include(wagtail_urls)),
]
# ... etc
```

You can copy templates to customise like this:

```
git clone https://github.com/pennersr/django-allauth.git django-allauth
cp -pr django-allauth/allauth/templates/* web/mysite/templates/
rm -rf django-allauth
```

You can use something like this in your templates:

```
    <body class="{% block body_class %}{% endblock %}">
      <p>
        <a href="{% slugurl 'home' %}">Home</a>

        {% if request.user.is_authenticated %}
          {{request.user.email}} (<a href="{% url 'account_email' %}">email</a>, <a href="{% url 'account_change_password' %}">password</a>{% if request.user.is_staff %}, <a href="{% url 'admin:index' %}">admin</a>, <a href="{% url 'wagtailadmin_home' %}">cms</a>{% endif %})
          <a href="{% url 'account_logout' %}">Sign out</a>
        {% else %}
          <a href="{% url 'account_login' %}">Sign in</a>
        {% endif %}
      </p>
      {% block messages %}
        {% if messages %}
          <div class="messages">
            <h3>Messages</h3>
            <ul class="messages">
                {% for message in messages %}
                <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
                {% endfor %}
            </ul>
          </div>
        {% endif %}
      {% endblock %}
      <div class="content">
        {% block content %}{% endblock %}
```

You can also customise lots of forms including:

```
ACCOUNT_FORMS (={})
Used to override forms, for example: {'login': 'mysite.forms.LoginForm'}

Possible keys (and default values):

add_email: allauth.account.forms.AddEmailForm
change_password: allauth.account.forms.ChangePasswordForm
disconnect: allauth.socialaccount.forms.DisconnectForm
login: allauth.account.forms.LoginForm
reset_password: allauth.account.forms.ResetPasswordForm
reset_password_from_key: allauth.account.forms.ResetPasswordKeyForm
set_password: allauth.account.forms.SetPasswordForm
signup: allauth.account.forms.SignupForm
signup: allauth.socialaccount.forms.SignupForm
```

One useful thing is to add a token (as long as it isn't for anything too critical as it could be changed maliciouly) to the email verification link so a user can carry on from where they left off. You can do so by customizing an `AccountAdapter`, creating a new URL route and then have it redirect to the usual verifiaction email link after setting a session cookie.


urls.py:

```
urlpatterns = [
    # ...
    path("confirm-email/<str:token>/<str:key>", views.confirm_email, name="confirm-email"),
    # ...
]
```

views.py:

```
def confirm_email(request, token, key):
    request.session['token'] = token
    url = reverse("account_confirm_email", args=[key])
    return redirect(url)
```

adapters.py:

```
from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpRequest
from django.urls import reverse

class TokenAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.
        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        if 'token' not in request.session:
            url = reverse("account_confirm_email", args=[emailconfirmation.key])
            return HttpRequest.build_absolute_uri(request, url)
        else:
            url = reverse("mysite:confirm-email",
                kwargs={'token':request.session['token'], 'key':emailconfirmation.key})
            return HttpRequest.build_absolute_uri(request, url)
```

settings:

```
ACCOUNT_ADAPTER = 'mysite.adapters.TokenAccountAdapter'
```

'''


if 'django.contrib.sites' not in INSTALLED_APPS:
    INSTALLED_APPS.append('django.contrib.sites')
if 'django.template.context_processors.request' not in TEMPLATES[0]['OPTIONS']['context_processors']:
    TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.request')

if 'AUTHENTICATION_BACKENDS' not in locals():
    AUTHENTICATION_BACKENDS = []

if 'django.contrib.auth.backends.ModelBackend' not in AUTHENTICATION_BACKENDS:
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.ModelBackend')
if 'allauth.account.auth_backends.AuthenticationBackend' not in AUTHENTICATION_BACKENDS:
    AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')
for app in [
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
for app in [
    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.agave',
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.angellist',
    # 'allauth.socialaccount.providers.asana',
    # 'allauth.socialaccount.providers.auth0',
    # 'allauth.socialaccount.providers.authentiq',
    # 'allauth.socialaccount.providers.baidu',
    # 'allauth.socialaccount.providers.basecamp',
    # 'allauth.socialaccount.providers.bitbucket',
    # 'allauth.socialaccount.providers.bitbucket_oauth2',
    # 'allauth.socialaccount.providers.bitly',
    # 'allauth.socialaccount.providers.cern',
    # 'allauth.socialaccount.providers.coinbase',
    # 'allauth.socialaccount.providers.dataporten',
    # 'allauth.socialaccount.providers.daum',
    # 'allauth.socialaccount.providers.digitalocean',
    # 'allauth.socialaccount.providers.discord',
    # 'allauth.socialaccount.providers.disqus',
    # 'allauth.socialaccount.providers.douban',
    # 'allauth.socialaccount.providers.draugiem',
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.dwolla',
    # 'allauth.socialaccount.providers.edmodo',
    # 'allauth.socialaccount.providers.eveonline',
    # 'allauth.socialaccount.providers.evernote',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.feedly',
    # 'allauth.socialaccount.providers.fivehundredpx',
    # 'allauth.socialaccount.providers.flickr',
    # 'allauth.socialaccount.providers.foursquare',
    # 'allauth.socialaccount.providers.fxa',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.gitlab',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.hubic',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.jupyterhub',
    # 'allauth.socialaccount.providers.kakao',
    # 'allauth.socialaccount.providers.line',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.mailru',
    # 'allauth.socialaccount.providers.mailchimp',
    # 'allauth.socialaccount.providers.meetup',
    # 'allauth.socialaccount.providers.microsoft',
    # 'allauth.socialaccount.providers.naver',
    # 'allauth.socialaccount.providers.nextcloud',
    # 'allauth.socialaccount.providers.odnoklassniki',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.openstreetmap',
    # 'allauth.socialaccount.providers.orcid',
    # 'allauth.socialaccount.providers.paypal',
    # 'allauth.socialaccount.providers.patreon',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.pinterest',
    # 'allauth.socialaccount.providers.reddit',
    # 'allauth.socialaccount.providers.robinhood',
    # 'allauth.socialaccount.providers.sharefile',
    # 'allauth.socialaccount.providers.shopify',
    # 'allauth.socialaccount.providers.slack',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.spotify',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.steam',
    # 'allauth.socialaccount.providers.strava',
    # 'allauth.socialaccount.providers.stripe',
    # 'allauth.socialaccount.providers.trello',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.twentythreeandme',
    # 'allauth.socialaccount.providers.twitch',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.untappd',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vimeo_oauth2',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.weibo',
    # 'allauth.socialaccount.providers.weixin',
    # 'allauth.socialaccount.providers.windowslive',
    # 'allauth.socialaccount.providers.xing',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

# This is a config for email only singin
# Don't require users to confirm their emails again when they click on a link
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# Choose a real URL:
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
if not DEBUG:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
SOCIALACCOUNT_STORE_TOKENS = False
ACCOUNT_USER_DISPLAY = lambda user: user.email
ACCOUNT_LOGOUT_ON_GET = True

# Add a Site for your domain in the Django Admin, matching settings.SITE_ID (django.contrib.sites app). I'm not sure why allauth needs this.
SITE_ID = 1
