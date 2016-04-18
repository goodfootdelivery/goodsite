#
#       Delivery API Serializers
#
#               Wed  2 Mar 17:05:09 2016
#

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Address, Parcel, Shipment, Order
from .services import GoogleService, EasypostService
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
            easypost_id = EasypostService.create_address(**data)
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
                data['rates'] = GoogleService.get_local_rates(str(pickup), str(dropoff))
            else:
                local_prices = GoogleService.get_local_rates(str(pickup))
                easypost_data = EasypostService.get_shipment_rates(
                    pickup = pickup.easypost_id,
                    dropoff = dropoff.easypost_id,
                    parcel = data.get('parcel'),
                    local_price = local_prices[0]['price']
                )
                print
                print easypost_data
                print
                data.update(easypost_data)
        except easypost.Error as e:
            print e.json_body['error']['code']
            # raise ValidationError({'Easypost Shipment Error': e})
            raise ValidationError({
                'Easypost Error': e.json_body['error']['message']
            })
        except Exception as e:
            raise ValidationError({'Shipment Creation Error': e})
        else:
            return data


### RATE SERIALIZER ###

class RateSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        print data
        rate_id = data.get('rate_id')
        order = data.get('order')
        shipment = data.get('shipment')
        #
        # Add Logic To Ensure Order Hasn't Been Purchased
        #
        try:
            if order.is_local:
                prices = GoogleService.get_local_rates(str(order.pickup), str(order.dropoff))
                if rate_id == 'BASIC':
                    data['rate'] = prices[0]['price']
                elif rate_id == 'EXPRESS':
                    data['rate'] = prices[1]['price']
                else:
                    raise ValidationError('Invalid Rate: Local Order')
            else:
                if not match(r'rate_.*', rate_id):
                    raise ValidationError('Invalid Rate: Non-Local Order')
                prices = GoogleService.get_local_rates(str(order.pickup))
                purchase = EasypostService.purchase_label(shipment.easypost_id, rate_id)
                data.update(purchase)
                data['price'] = purchase['cost'] + prices[0]['price']
        except easypost.Error as e:
            raise ValidationError({
                'Easypost Error': e.json_body['error']['message']
            })


        except ObjectDoesNotExist as e:
            raise ValidationError({'order': 'Order id required.'})
        except TypeError as e:
            raise ValidationError({'rate': e})
        else:
            return data
        # except Exception as e:
        #     raise ValidationError({'ERROR': e})

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
