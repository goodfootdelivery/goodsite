#
#   Invoice Module
#
#           Tue 22 Mar 12:57:54 2016
#

from refreshbooks import api

# Production
# COMPANY = 'Good Foot Support Services (Good Foot Delivery)'
# FB_URL = 'goodfootdelivery.freshbooks.com'
# API_KEY = '1dc85e1ad7a0ac4a9840e4687e94ac20'

# Testing
COMPANY = 'Goodfoot Delivery Gamma'
FB_URL = 'goodfootdeliverygamma.freshbooks.com'
API_KEY = '0e7d9e834a671c665ada820250babc01'


def create_client(first_name, last_name, email):
    print '\t __Creating Client__'
    try:
        fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
        client = fb.client.create(
            client={
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        )
        return client.client_id
    except Exception as e:
        print e
        return None
    finally:
        print '\n'


def create_invoice(client_id):
    print '\t __Creating Invoice__'
    try:
        fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
        resp = fb.invoice.create(
            invoice = {
                'client_id': client_id
            }
        )
        return resp.invoice_id
    except Exception as e:
        print e
        return None
    finally:
        print '\n'

def add_line(invoice_id):
    fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
    fb.invoice.lines.add(
        invoice_id = invoice_id,
        lines = [
            api.types.line(
                name='test order',
                unit_cost=40.00,
                quantity=1
            )
        ]
    )


if __name__ == '__main__':
    # my_id =  create_client('connor', 'sullivan', 'sully4792@gmail.com')
    my_invoice = create_invoice(133743)

    fb = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)
    invoice_resp = fb.invoice.get(invoice_id = my_invoice)
    add_line(invoice_resp.invoice.invoice_id)

    print "New invoice created: #%s (id %s)" % (
        invoice_resp.invoice.number,
        invoice_resp.invoice.invoice_id
    )

    print my_invoice
