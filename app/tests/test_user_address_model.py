import unittest

import django.test
from django.core.management import call_command


class TestCase(django.test.TestCase):

    def setUp(self):
        super().setUp()
        call_command('loaddata', 'initial_data.json', verbosity=0)


if __name__ == '__main__':
    unittest.main()
