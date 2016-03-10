#
#       Delivery API Serializers
#
#               Wed  2 Mar 17:05:09 2016
#

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Address, Parcel, Order


### ADDRESS SERIALIZER ###

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ( 'id', 'street', 'unit', 'postal', 'prov', 'country',
                  'city', 'name', 'phone', )


### PARCEL SERIALIZER ###

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('length', 'height', 'width', 'weight')


### ORDER SERIALIZER ###

class OrderSerializer(serializers.ModelSerializer):
    pickup = serializers.PrimaryKeyRelatedField(
        queryset = Address.objects.all()
    )
    dropoff = serializers.PrimaryKeyRelatedField(
        queryset = Address.objects.all()
    )
    parcel = ParcelSerializer()
    easypost_id = serializers.ReadOnlyField()
    tracking_code = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ( 'id', 'pickup', 'dropoff', 'parcel', 'order_date', 'easypost_id',
                        'price', 'delivery_date', 'service', 'tracking_code' )
        depth = 1

    def create(self, validated_data):
        package = validated_data.pop('parcel', None)
        parcel = Parcel.objects.create(**package)
        return Order(parcel=parcel, **validated_data)


### RATE SERIALIZER ###

class RateSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        rate_id = data.get('rate_id')
        # Apply Regex for Local and Easypost Rate Formats
        return { 'rate_id': rate_id }

    def update(self, instance, validated_data):
        rate = validated_data.get('rate_id')
        if instance.purchase(rate):
            instance.save()
            return {
                'status': 'SUCCESS',
            }
        else:
            return { 'error': 'Invalid Rate' }

