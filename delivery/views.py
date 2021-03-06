#
#       Delivery API Views
#
#               Wed  2 Mar 17:05:09 2016
#
from rest_framework.decorators import detail_route
from rest_framework.response import Response
# from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_framework import viewsets

from .models import Address, Order
from .serializers import AddressSerializer, OrderSerializer, RateSerializer
from .permissions import IsOwnerOrReadOnly

TEST_EP_KEY = 'yARJbUTstAI0WNeVQLxK4g'


# ADDRESS VIEWS

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ORDER VIEWS

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=self.request.user)
        rates = order.get_rates()
        order.save()
        data = {
            'order': serializer.data,
            'rates': rates,
        }
        return Response(data, status=201)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def update(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        serializer = RateSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        data = {
            "order": order.id,
            "price": order.price
        }
        return Response(data)
