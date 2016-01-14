from django.contrib import admin
from .models import Order, Address

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    pass
    # exclude = ['dist_mat', 'status']
    # list_display = ['user', 'order_date', 'courier', 'get_duration']
    # list_filter = ['order_date', 'user', 'courier']


class AddressAdmin(admin.ModelAdmin):
    pass
    # form = AddressForm
    # exclude = ['location']
    # list_display = ['user', 'address', 'contact_name', 'contact_number']

admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
