#
#   Invoice Module
#
#           Tue 22 Mar 12:57:54 2016
#

from refreshbooks import api

COMPANY = 'Good Foot Support Services (Good Foot Delivery)'
FB_URL = 'goodfootdelivery.freshbooks.com'
API_KEY = '1dc85e1ad7a0ac4a9840e4687e94ac20'
API_N = 'dc85e1ad7a0ac4a9840e4687e94ac20'

if __name__ == '__main__':
    api = api.TokenClient(FB_URL, API_KEY, user_agent=COMPANY)

    me = api.client.create(
        client={
            'email': 'connor.sullivan@mail.mcgill.ca'
        }
    )

    my_id =  me.client_id

    try:
        invoice_resp = api.invoice.list()
        print '### Invoice List ### \n'
        for invoice in invoice_resp.invoices.invoice:
            print "Invoice %s Total: %s" % ( invoice.invoice_id, invoice.amount )

        api.invoice.create(
            invoice = {
                'client_id': my_id
            }
        )
        invoice_new = api
    except Exception as e:
        print e
    finally:
        print '\n'

    # try:
    #     client_resp = api.client.list()
    #     print '### Client List ### \n'
    #     for client in client_resp.clients.client:
    #         print "First Name %s, Last Name: %s, Org: %s" % \
    #             ( client.first_name, client.last_name, client.organization )

    # except Exception as e:
    #     print e
    # finally:
    #     print '\n'

