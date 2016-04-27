from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from delivery import views

from django.contrib import admin


urlpatterns = [

    url(r'^grappelli/', include('grappelli.urls')),
    url(r"^admin/", include(admin.site.urls)),
    # url(r"^account/", include("account.urls")),
    url(r'^auth/', include('rest_auth.urls')),

    # API
    url(r'^delivery/', include('delivery.urls')),
    url(r'^invoicing/', include('invoicing.urls')),
    # Goodfoot
]

router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet, 'address')
router.register(r'orders', views.OrderViewSet, 'order')

urlpatterns += router.urls

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
