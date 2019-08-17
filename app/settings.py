import os


SECRET_KEY = 'test'

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

FIXTURE_DIRS = (
   os.path.join(ROOT_PATH, 'tests', 'fixtures'),
)

INSTALLED_APPS = (
    'app_address',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
