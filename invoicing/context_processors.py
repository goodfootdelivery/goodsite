# Invoicing Context Processor

from .models import Client

def invoice(request):
    try:
        client = Client.objects.get(user=request.user)
        return {'client': client.id}
    except:
        return {}
