from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address, Parcel, Order



class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='delivery:user-detail')

    class Meta:
        model = User
        fields = ('user', 'addresses')
        extra_kwargs = {
            'addresses': {'view_name': 'delivery:address-detail'}
        }


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='delivery:address-detail')

    class Meta:
        model = Address
        fields = ('address', 'link')

    def validate_address(self, data):
        if data is None:
            raise serializers.ValidationError('No Address Given')
        ad = data.split(',')
        if ad.__len__() != 4:
            raise serializers.ValidationError('Incorrect Address Format')
        elif ad[0].split().__len__() != 3:
            raise serializers.ValidationError('Incomplete Street Information')
        elif ad[2].split().__len__() != 3:
            raise serializers.ValidationError('Incomplete Postal Information')
        elif ad[3] != ' Canada':
            raise serializers.ValidationError('Addresses Within Canada Only')
        return data


class ParcelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        pass
    pass


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    pickup = serializers.HyperlinkedRelatedField(
        view_name = 'delivery:address-detail',
        queryset = Address.objects.all()
    )
    dropoff = serializers.HyperlinkedRelatedField(
        view_name = 'delivery:address-detail',
        queryset = Address.objects.all()
    )
    parcel = ParcelSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('order_date', 'delivery_date', 'service', 'pickup', 'dropoff', 'parcel')
