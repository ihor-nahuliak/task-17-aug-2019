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

    def test_full_address_1(self):
        m = UserAddress.objects.get(id=1)
        m.save()
        self.assertEqual(m.full_address,
                         '\nNone\nNone Giventown None ')

    def test_full_address_2(self):
        m = UserAddress.objects.get(id=2)
        m.save()
        self.assertEqual(m.full_address,
                         'Randomstreet\nNone\nNone Giventown None ')

    def test_full_address_3(self):
        m = UserAddress.objects.get(id=3)
        m.save()
        self.assertEqual(m.full_address,
                         '456 Randomstreet\nNone\nNone Giventown None ')

    def test_full_address_4(self):
        m = UserAddress.objects.get(id=4)
        m.save()
        self.assertEqual(m.full_address,
                         '789 Otherstreet\nNone\nNone Giventown None NL')


if __name__ == '__main__':
    unittest.main()
