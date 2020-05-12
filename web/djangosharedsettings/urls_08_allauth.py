from django.contrib import admin
from django.urls import include, path
from django.urls import path, re_path, include


from django.views.generic.base import RedirectView


orig_patterns = []
while urlpatterns:
    orig_patterns.append(urlpatterns.pop(0))

app_name = 'myactualsite'
urlpatterns += [
    path('accounts/', include('allauth.urls')),
    # Optionally hide all the other login screens by redirecting them to the one above
    # path('cms/login/', RedirectView.as_view(url='/accounts/login', query_string=True, permanent=False), name='index'),
    # path('_util/login/', RedirectView.as_view(url='/accounts/login', query_string=True, permanent=False), name='index'),
    # path('admin/login/', RedirectView.as_view(url='/accounts/login', query_string=True, permanent=False), name='index'),
]
urlpatterns += orig_patterns
