from .base import *

SECRET_KEY = 'django-insecure-j__^r-dso#ok_*5+%j(a@u66_^ca@p&a04!1x*mqeauwvzvyi#'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db-development.sqlite3'
    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, "html/static")]
