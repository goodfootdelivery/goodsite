from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address, Parcel, Order

import googlemaps
import easypost

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
OFFICE = '720 Bathurst St, Toronto, ON M5S 2R4, CA'


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='address-detail')

    class Meta:
        model = Address
        fields = ( 'street', 'link', 'postal_code', 'region', 'country',
                  'city', 'contact_name', 'contact_number', )

    def validate_country(self, value):
        if not value.upper() == 'CA':
            raise serializers.ValidationError('We currently only ship within Canada.')
        return value


class ParcelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parcel
        fields = ('length', 'height', 'width', 'weight')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    tracking_code = serializers.ReadOnlyField()
    postal_label = serializers.ReadOnlyField()
    pickup = serializers.HyperlinkedRelatedField(
        view_name = 'address-detail',
        queryset = Address.objects.all()
    )
    dropoff = serializers.HyperlinkedRelatedField(
        view_name = 'address-detail',
        queryset = Address.objects.all()
    )
    parcel = ParcelSerializer()

    class Meta:
        model = Order
        fields = ( 'pickup', 'dropoff', 'parcel', 'order_date',
                    'delivery_date', 'service', 'tracking_code', 'postal_label')
        depth = 1

    def create(self, validated_data):
        package = validated_data.pop('parcel', None)
        parcel = Parcel.objects.create(
            length = package.get('length'),
            width = package.get('width'),
            height = package.get('height'),
            weight = package.get('weight'),
        )
        order = Order(parcel=parcel, **validated_data)
        order.save()
        return order

    def validate_pickup(self, value):
        if not value.city == 'Toronto':
            raise serializers.ValidationError(
                'Can only pickup in Toronto'
            )
        else:
            return value

    def validate(self, data):
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        client = googlemaps.Client(key=GKEY)

        if not dropoff.city == 'Toronto':
            destination = OFFICE
        else:
            destination = dropoff.formatted()

        trip = client.distance_matrix(
            pickup.formatted(),
            destination,
            mode = 'transit'
        )

        if not trip['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
            return data
        else:
            raise serializers.ValidationError(
                'Please Ensure both addresses are valid and try again'
            )
