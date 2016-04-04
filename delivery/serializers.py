#
#       Delivery API Serializers
#
#               Wed  2 Mar 17:05:09 2016
#

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Address, Parcel, Shipment, Order
from .delivery import get_prices, OFFICE

import easypost

# Authenticate EasyPost Instance
TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'
easypost.api_key = TEST_EP_KEY

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
        print "\n Create Object: \n"
        print type(validated_data)
        print validated_data
        # Pop off Nested Fields
        package = validated_data.pop('parcel')
        easypost_id = validated_data.pop('easypost_id', None)
        rates = validated_data.pop('rates', None)
        if easypost_id:
            shipment = Shipment.objects.create(easypost_id=easypost_id)
        else:
            shipment = None
        # Create Nested Object
        parcel = Parcel.objects.create(**package)
        order = Order.objects.create(parcel=parcel, shipment=shipment, **validated_data)
        order.rates = rates
        return order

    def validate_pickup(self, value):
        if not value.is_local():
            raise ValidationError('Pickup Address Not Local')
        return value

    def validate(self, data):
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        if dropoff.is_local():
            data['rates'] = get_prices(pickup.__str__(), dropoff.__str__())
        else:
            try:
                shipment = easypost.Shipment.create(
                    from_address = pickup.easypost(),
                    to_address = dropoff.easypost(),
                    parcel = data.get('parcel')
                )
                if not shipment.rates:
                    raise Exception
                prices = get_prices(pickup.__str__(), OFFICE)
                # Polish Rate Function
                def format_rates(rate):
                    price = float(rate.rate) + prices[0]['price']
                    return {
                        'id': rate.id,
                        'carrier': rate.carrier,
                        'service': rate.service,
                        'rate': str(price),
                        'days': rate.delivery_days
                    }
                data['easypost_id'] = shipment.id
                data['rates'] = map(format_rates, shipment.rates)
            except Exception as e:
                raise ValidationError(e)
        return data


### RATE SERIALIZER ###

class RateSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        rate_id = data.get('rate_id')
        # Apply Regex for Local and Easypost Rate Formats
        return { 'rate_id': rate_id }

    def update(self, instance, validated_data):
        rate = validated_data.get('rate_id')
        if instance.purchase(rate) is not None:
            instance.save()
            return instance
        else:
            return instance
