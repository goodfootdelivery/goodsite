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
        order = Order.objects.create(parcel=parcel, **validated_data)
        return order


### RATE SERIALIZER ###

class RateSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        if instance.is_local():
            raise ValidationError('Shipment Doesn\'t require Easypost')

        rates = instance.easypost()
        if not rates:
            raise ValidationError('Invalid Shipment')
        instance.save()
        return rates

    def to_internal_value(self, data):
        rate_id = data.get('rate_id')
        instance = Order.objects.get(pk=data.get('pk'))
        if not instance.purchase(rate_id):
            raise ValidationError('Invalid Rate')
        else:
            instance.save()
            return {
                'rate_id': instance.rate_id,
                'easypost_id': instance.easypost_id,
                'tracking_code': instance.tracking_code,
                'postal_label': instance.postal_label,
                'status': 'SUCCESS'
            }
