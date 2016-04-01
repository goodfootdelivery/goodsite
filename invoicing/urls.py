from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.contrib import admin
from .views import BalanceView, HistoryView, ClientView


urlpatterns = [
    url(r'^balance/$', login_required(BalanceView.as_view()), name='balance'),
    url(r'^history/$', login_required(HistoryView.as_view()), name='history'),
    url(r'^client/(?P<pk>\d+)/$', login_required(ClientView.as_view()), name='client'),
]
