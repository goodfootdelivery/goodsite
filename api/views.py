from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_framework import viewsets

from .models import Address, Order
from .serializers import AddressSerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly

import easypost
TEST_EP_KEY = 'yARJbUTstAI0WNeVQLxK4g'


# ADDRESS VIEWS

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ORDER VIEWS

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        return Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route(methods=['GET', 'POST'])
    def get_rates(self, request, pk=None):
        if request.method == 'GET':
            # order = self.get_object()
            # OR
            # order = Order.objects.get(pk)

            # EASYPOST STUFF

            # serializer = RateSerializer(rates)
            # RETURN RATES
            pass
        if request.method == 'POST':
            # BUY RATE
            # COMPLETE ORDER INFO
            pass
        pass
