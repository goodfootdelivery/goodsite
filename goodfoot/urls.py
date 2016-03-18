from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.contrib import admin
from . import views


urlpatterns = [
    # url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r'^$', login_required(views.DeliveryView.as_view()), name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^payments/", include("pinax.stripe.urls")),

    # API
    url(r'^api/', include('applications.delivery.urls')),
    url(r'^placeorder/$', login_required(views.DeliveryView.as_view()), name='delivery'),
    url(r'^hub/$', login_required(views.HubView.as_view()), name='hub'),

    # Goodfoot
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
