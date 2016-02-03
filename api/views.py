from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_framework import viewsets

from .models import Address, Order
from .serializers import AddressSerializer, OrderSerializer, RateSerializer
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
    def rates(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        # order = self.get_object()

        if request.method == 'GET':
            print 'get method'
            serializer = RateSerializer(order)
            print 'hererere'
            print serializer.data
            return Response(serializer.data)

        if request.method == 'POST':
            print 'post method'
            serializer = RateSerializer(order, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.validated_data)
