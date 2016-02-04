from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Address, Parcel, Order

import easypost
TEST_EP_KEY = 'OJwynagQo2hRGHBnKbAiHg'

import googlemaps
GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'



### ADDRESS SERIALIZER ###

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


### PARCEL SERIALIZER ###

class ParcelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parcel
        fields = ('length', 'height', 'width', 'weight')


### ORDER SERIALIZER ###

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='order-detail')
    shipmenting_id = serializers.ReadOnlyField()
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
        fields = ( 'link', 'pickup', 'dropoff', 'parcel', 'order_date', 'shipmenting_id',
                        'delivery_date', 'service', )
        depth = 1

    def create(self, validated_data):
        package = validated_data.pop('parcel', None)
        parcel = Parcel.objects.create(**package)
        pickup = validated_data['pickup']
        dropoff = validated_data['dropoff']

        easypost.api_key = TEST_EP_KEY

        try:
            shipment = easypost.Shipment.create(
                from_address = pickup.easypost,
                to_address = dropoff.easypost,
                parcel= package
            )
            shipmenting_id = shipment.id
        except Exception as e:
            raise ValidationError(e)

        order = Order.objects.create(
            parcel = parcel,
            shipmenting_id = shipmenting_id,
            **validated_data
        )
        return order

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


### RATE SERIALIZER ###

class RateSerializer(serializers.BaseSerializer):
    easypost.api_key = TEST_EP_KEY

    def to_representation(self, obj):
        try:
            shipment = easypost.Shipment.retrieve(obj.shipping_id)
        except Exception as e:
            raise ValidationError(e)

        rates = []
        for rate in shipment.rates:
            rates.append(rate.id)

        return rates

    def to_internal_value(self, data):
        rate_id = data.get('rate_id')
        shipping_id = data.get('shipping_id')

        # EasyPost Retrieval & Purchase
        try:
            shipment = easypost.Shipment.retrieve(shipping_id)
            purchase = shipment.buy(rate={ 'id': rate_id })
        except Exception as e:
            raise ValidationError(e)

        return {
            'rate_id': rate_id,
            'shipping_id': shipping_id,
            'postal_label': purchase.postage_label.label_url,
            'tracking_code': purchase.tracking_code
        }

    def update(self, instance, validated_data):
        instance.rate_id = validated_data.get('rate_id')
        instance.postal_label = validated_data.get('postal_label')
        instance.tracking_code = validated_data.get('tracking_code')

        instance.save()
        return instance
