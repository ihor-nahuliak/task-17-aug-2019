import unittest

import django.test
from django.core.management import call_command

from app_address.models import UserAddress


class TestCase(django.test.TestCase):

    def setUp(self):
        super().setUp()
        call_command('loaddata', 'initial_data.json', verbosity=0)

    def test_model_attributes_list(self):
        self.assertTrue(hasattr(UserAddress, 'user'))
        self.assertTrue(hasattr(UserAddress, 'name'))
        self.assertTrue(hasattr(UserAddress, 'street_address'))
        self.assertTrue(hasattr(UserAddress, 'street_address_line2'))
        self.assertTrue(hasattr(UserAddress, 'zipcode'))
        self.assertTrue(hasattr(UserAddress, 'city'))
        self.assertTrue(hasattr(UserAddress, 'state'))
        self.assertTrue(hasattr(UserAddress, 'country'))
        self.assertTrue(hasattr(UserAddress, 'full_address'))


if __name__ == '__main__':
    unittest.main()
