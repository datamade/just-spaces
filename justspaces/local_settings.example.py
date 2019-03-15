# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'very secret key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'just-spaces',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'database',
        'PORT': '5432',
    }
}
