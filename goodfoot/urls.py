# Root URLs for Goodfoot
# Sat Jan  9 16:34:39 2016

from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    # Overhead
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^account/', include('account.urls')),

    # API
    url(r'^api/', include('delivery.urls')),

    # Goodfoot
    url(r'^$', views.HomeView.as_view(), name='home'),
]
