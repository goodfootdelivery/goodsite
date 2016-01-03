from rest_framework import serializers
from .models import Address, Parcel, Order


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('contact_name', 'contact_number', 'address', 'unit', 'location', 'comments')


class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('length', 'height', 'width', 'weight')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_date', 'delivery_date', 'status', 'service', 'pickup', 'dropoff', 'parcel')
