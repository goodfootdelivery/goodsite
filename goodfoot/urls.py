# Root URLs for Goodfoot
# Sat Jan  9 16:34:39 2016

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views


urlpatterns = [
    # Overhead
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^account/', include('account.urls')),

    # API
    url(r'^api/', include('api.urls')),

    # Goodfoot
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^delivery/$', views.DeliveryView.as_view(), name='delivery'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
