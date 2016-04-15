#
#       Delivery API Serializers
#
#               Wed  2 Mar 17:05:09 2016
#

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Address, Parcel, Shipment, Order
from . import services
from re import match

import easypost

# Authenticate EasyPost Instance
TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'
easypost.api_key = TEST_EP_KEY

### ADDRESS SERIALIZER ###

class AddressSerializer(serializers.ModelSerializer):
    easypost_id = serializers.ReadOnlyField()
    class Meta:
        model = Address
        fields = ( 'id', 'easypost_id', 'street', 'unit', 'postal', 'prov', 'country',
                  'city', 'name', 'phone', )

    def validate(self, data):
        # if self.city.upper() == 'TORONTO':
        #     return data
        # else:
        try:
            easypost_id = services.create_address(**data)
            data.update({'easypost_id':easypost_id})
        except Exception as e:
            raise ValidationError({'Easypost Address Error': e})
        return data


### PARCEL SERIALIZER ###

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('length', 'height', 'width', 'weight')


### ORDER SERIALIZER ###

class OrderSerializer(serializers.ModelSerializer):
    pickup = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    dropoff = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    # pickup = AddressSerializer()
    # dropoff = AddressSerializer()
    parcel = ParcelSerializer()
    service = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()
    rates = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ( 'id', 'pickup', 'dropoff', 'parcel', 'order_date',
                        'price', 'delivery_date', 'service', 'rates')
        depth = 1

    def create(self, validated_data):
        package = validated_data.pop('parcel')
        easypost_id = validated_data.pop('easypost_id', None)
        rates = validated_data.pop('rates', None)
        # Create Nested Object
        parcel = Parcel.objects.create(**package)
        order = Order.objects.create(parcel=parcel, **validated_data)
        if easypost_id:
            Shipment.objects.create(order=order, easypost_id=easypost_id)
        order.rates = rates
        return order

    def validate_pickup(self, value):
        if not value.is_local():
            raise ValidationError('Pickup Address Not Local')
        return value

    def validate(self, data):
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        try:
            if dropoff.is_local():
                data['rates'] = services.get_local_rates(str(pickup), str(dropoff))
            else:
                print
                print 'Address Types:', type(pickup), type(dropoff)
                print 'Address Values:', pickup, dropoff
                print
                easypost_data = services.get_non_local_rates(
                    pickup = pickup,
                    dropoff = dropoff,
                    parcel = data.get('parcel')
                )
                data.update(easypost_data)
        except easypost.Error as e:
            raise ValidationError({'Easypost Shipment Error': e})
        return data


### RATE SERIALIZER ###

class RateSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        rate_id = data.get('rate_id')
        service = data.get('service')
        order_id = data.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            if match(r'rate_.*', rate_id):
                if order.is_local:
                    raise ValidationError('Invalid Rate: Local Order')
                prices = services.get_local_rates(str(order.pickup), services.OFFICE)
                purchase = services.purchase_label(order.easypost_id, rate_id)
                data.update(purchase)
            if not order.is_local:
                raise ValidationError('Invalid Rate: Non-Local Order')
            prices = services.get_local_rates(str(order.pickup), str(order.dropoff))
            if rate_id == 'BASIC':
                data['rate'] = prices[0]['price']
            elif rate_id == 'EXPRESS':
                data['rate'] = prices[1]['price']
            else:
                raise ValidationError('Incorrect Rate Format')
            # Apply Regex for Local and Easypost Rate Formats
            return data
        except easypost.Error as e:
            raise ValidationError({'Easypost Purchase Error': e})
        except ObjectDoesNotExist as e:
            raise ValidationError({'order': 'Order id required.'})
        except TypeError as e:
            raise ValidationError({'rate': e})

    def update(self, instance, validated_data):
        if instance.is_local:
            Shipment.objects.filter(order=instance).update(
                cost = validated_data.pop('cost', None),
                postal_label = validated_data.pop('postal_label', None),
                tracking_code = validated_data.pop('tracking_code', None),
            )
        instance.price = validated_data.pop('rate', None)
        instance.save()
        return instance
