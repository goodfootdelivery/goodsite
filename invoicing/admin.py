from django.contrib import admin
from .models import Client, Invoice

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Client, ClientAdmin)
# admin.site.register(Invoice, InvoiceAdmin)
