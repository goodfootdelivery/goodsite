from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'courier')
    list_filter = ['order_date', 'user', 'courier']

admin.site.register(Order, OrderAdmin)

# admin.site.register(OrderMeta, OrderMetaAdmin)
