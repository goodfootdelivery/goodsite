from django.conf.urls import include, url
# from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.set_addr, name='placeorder'),
    url(r'^confirm/$', views.confirmorder, name='confirmorder'),
    url(r'^success/$', views.success, name='success'),
]
