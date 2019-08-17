import unittest

import django.test
from django.db import IntegrityError
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
        m = UserAddress(user_id=1,
                        name='Max',
                        city='Giventown')
        m.save()
        self.assertEqual(m.full_address,
                         '\nNone\nNone Giventown None ')

    def test_full_address_2(self):
        m = UserAddress(user_id=1,
                        name='Max Mustermann',
                        street_address='Randomstreet',
                        city='Giventown')
        m.save()
        self.assertEqual(m.full_address,
                         'Randomstreet\nNone\nNone Giventown None ')

    def test_full_address_3(self):
        m = UserAddress(user_id=1,
                        name='Max Mustermann',
                        street_address='456 Randomstreet',
                        city='Giventown')
        m.save()
        self.assertEqual(m.full_address,
                         '456 Randomstreet\nNone\nNone Giventown None ')

    def test_full_address_4(self):
        m = UserAddress(user_id=1,
                        name='Max Mustermann',
                        street_address='789 Otherstreet',
                        city='Giventown',
                        country='NL')
        m.save()
        self.assertEqual(m.full_address,
                         '789 Otherstreet\nNone\nNone Giventown None NL')

    def test_deduplication_leaves_just_2_unique_records(self):
        m = UserAddress(user_id=1,
                        name='Max',
                        city='Giventown')
        m.save()
        m = UserAddress(user_id=1,
                        name='Max Mustermann',
                        street_address='Randomstreet',
                        city='Giventown')
        m.save()
        m = UserAddress(user_id=1,
                        name='Max Mustermann',
                        street_address='456 Randomstreet',
                        city='Giventown')
        m.save()
        m = UserAddress(user_id=1,
                        name='Max Mustermann',
                        street_address='789 Otherstreet',
                        city='Giventown',
                        country='NL')
        m.save()
        total_count = UserAddress.objects.count()

        self.assertEqual(2, total_count)

    def test_deduplication_raises_conflict_error_on_different_pk(self):
        m = UserAddress(id=1,
                        user_id=1,
                        name='Max',
                        city='Giventown')
        m.save()
        m = UserAddress(id=2,
                        user_id=1,
                        name='Max Mustermann',
                        street_address='Randomstreet',
                        city='Giventown')
        with self.assertRaises(IntegrityError) as err_ctx:
            m.save()

        self.assertEqual(err_ctx.exception.args[0], 'address duplicated error')

    def test_match__name_not_filled(self):
        m1 = UserAddress(user_id=1, name='')
        m1.save()
        m2 = UserAddress(user_id=1, name='lorem ipsum dolor')
        m2.save()

        self.assertEqual(m2.id, m1.id)

    def test_match__name_filled_left(self):
        m1 = UserAddress(user_id=1, name='lorem')
        m1.save()
        m2 = UserAddress(user_id=1, name='lorem ipsum dolor')
        m2.save()

        self.assertEqual(m2.id, m1.id)

    def test_match__name_filled_center(self):
        m1 = UserAddress(user_id=1, name='ipsum')
        m1.save()
        m2 = UserAddress(user_id=1, name='lorem ipsum dolor')
        m2.save()

        self.assertEqual(m2.id, m1.id)

    def test_match__name_filled_right(self):
        m1 = UserAddress(user_id=1, name='dolor')
        m1.save()
        m2 = UserAddress(user_id=1, name='lorem ipsum dolor')
        m2.save()

        self.assertEqual(m2.id, m1.id)

    def test_match__name_filled_fully_duplicated(self):
        m1 = UserAddress(user_id=1, name='lorem ipsum dolor')
        m1.save()
        m2 = UserAddress(user_id=1, name='lorem ipsum dolor')
        m2.save()

        self.assertEqual(m2.id, m1.id)

    # def test_match__name_filled_better_before(self):
    #     # TODO: it takes the longest old value as a better one ???
    #     m1 = UserAddress(user_id=1, name='lorem ipsum dolor')
    #     m1.save()
    #     m2 = UserAddress(user_id=1, name='lorem ipsum')
    #     m2.save()
    #
    #     self.assertEqual(m2.id, m1.id)
    #     self.assertEqual(m2.name, 'lorem ipsum dolor')


if __name__ == '__main__':
    unittest.main()
