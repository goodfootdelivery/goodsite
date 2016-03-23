#
#   Invoice Module
#
#           Tue 22 Mar 12:57:54 2016
#

from refreshbooks import api

API_URL = 'https://goodfootdelivery.freshbooks.com/api/2.1/xml-in'
API_KEY = '1dc85e1ad7a0ac4a9840e4687e94ac20'

if __name__ == '__main__':
    client = api.TokenClient(
        'goodfootdelivery.freshbooks.com',
        API_KEY
    )

    print client
