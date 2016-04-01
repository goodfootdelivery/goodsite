from django.contrib import admin
from .models import Order, Address

# Register your models here.


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
    # form = AddressForm
    # exclude = ['location']
    # list_display = ['user', 'address', 'contact_name', 'contact_number']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
    # exclude = ['dist_mat', 'status']
    # list_display = ['user', 'order_date', 'courier', 'get_duration']
    # list_filter = ['order_date', 'user', 'courier']
