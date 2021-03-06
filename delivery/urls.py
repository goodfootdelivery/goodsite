from django.conf.urls import url, include
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet, 'address')
router.register(r'orders', views.OrderViewSet, 'order')

urlpatterns = router.urls
