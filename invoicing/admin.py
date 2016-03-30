from django.contrib import admin
from .models import Client, Invoice

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    pass

class InvoiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)
admin.site.register(Invoice, InvoiceAdmin)
