# Invoicing Context Processor

from .models import Client
import datetime

def invoice(request):
    try:
        print request.user
        client = Client.objects.get(user=request.user)
        return {
            'client_id': client.id,
            'is_open': True
        }
    except:
        pass
    finally:
        date = datetime.datetime.now()
        is_open = False
        if 9 <= date.hour <= 16:
            is_open = True
        return {
            'client_id': 'test',
            'is_open': is_open
        }
