from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import (ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView)

from .models import Address, Order
from .serializers import AddressSerializer, UserSerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShipmentViewSet(viewsets.ModelViewSet):
    def perform_create(self):
        # Create Easypost Shipment
        pass
    pass


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET', 'POST'])
def check_trip(request):
    if request.method == 'GET':
        print type(request.data)
        return Response([
            { 'type': request.content_type, },
            { 'data': request.data }
        ])
