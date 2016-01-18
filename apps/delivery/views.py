from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_framework import viewsets

from .models import Address, Order, Shipment
from .serializers import AddressSerializer, OrderSerializer, ShipmentSerializer
from .permissions import IsOwnerOrReadOnly

import easypost
TEST_EP_KEY = 'yARJbUTstAI0WNeVQLxK4g'


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
    serializer_class = ShipmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Shipment.objects.all()

    def perform_create(self, serializer):
        pickup = serializer.validated_data['pickup']
        dropoff = serializer.validated_data['dropoff']
        parcel = serializer.validated_data['parcel']

        if dropoff.city == 'Toronto':
            serializer.save()
            return

        easypost.api_key = TEST_EP_KEY

        shipment = easypost.Shipment.create(
            from_address = pickup.easypost,
            to_address = dropoff.easypost,
            parcel={
                'length': parcel.get('length'),
                'width': parcel.get('width'),
                'height': parcel.get('height'),
                'weight': parcel.get('weight'),
            }
        )

        if not shipment.rates:
            raise ValidationError('Invalid Shipment')
        else:
            shipment.buy(
                rate = {'id': shipment.rates[0].id}
            )
            serializer.save(
                tracking_code = shipment.tracking_code,
                postal_label = shipment.postage_label.label_url
            )


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
