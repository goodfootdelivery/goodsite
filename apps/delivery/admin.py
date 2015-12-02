from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'date', 'courier')
    list_filter = ['date', 'user_id', 'courier']

admin.site.register(Order, OrderAdmin)


class OrderMetaAdmin(admin.ModelAdmin):
    pass

# admin.site.register(OrderMeta, OrderMetaAdmin)
