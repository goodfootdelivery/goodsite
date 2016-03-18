from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

USER = 'sully'
PSWD = 'koncluv102'
# Create your tests here.


class AddressTest(APITestCase):
    def setUp(self):
        # John, ID_1
        self.user = User.objects.create_user(username='john', email='john@snow.com', password='johnpassword')
        self.client.login(username='john', password='johnpassword')
        # Jane, ID_2
        self.user = User.objects.create_user(username='jane', email='jane@snow.com', password='janepassword')
        self.client.login(username='jane', password='janepassword')

    def test_address_list(self):
        url = reverse('address-list')
        request = self.client.get(url, format='json')
        print request.data
