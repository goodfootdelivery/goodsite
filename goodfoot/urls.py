# Root URLs for Goodfoot
# Sat Jan  9 16:34:39 2016

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    # Overhead
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^account/', include('account.urls')),
    url(r'^billing/', include('pinax.stripe.urls')),

    # API
    url(r'^api/', include('api.urls')),
    url(r'^hub/$', login_required(views.HubView.as_view()), name='hub'),

    # Goodfoot
    url(r'^$', login_required(views.HomeView.as_view()), name='home'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
