"""
Django settings for justspaces project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from .local_settings import SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASES
import gettext

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'users',
    'surveys',

    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'crispy_forms',
    'widget_tweaks',

    # django-pldp
    'countries_plus',
    'languages_plus',
    'pldp',

    # fobi core
    'fobi',

    # fobi theme
    'fobi.contrib.themes.foundation5',
    'fobi_custom.override_theme',

    # fobi content form elements
    'fobi.contrib.plugins.form_elements.content.content_text',

    # fobi default form field plug-ins
    'fobi.contrib.plugins.form_elements.fields.boolean',
    'fobi.contrib.plugins.form_elements.fields.checkbox_select_multiple',
    'fobi.contrib.plugins.form_elements.fields.date',
    'fobi.contrib.plugins.form_elements.fields.float',
    'fobi.contrib.plugins.form_elements.fields.radio',
    'fobi.contrib.plugins.form_elements.fields.select',
    'fobi.contrib.plugins.form_elements.fields.text',
    'fobi.contrib.plugins.form_elements.fields.textarea',
    'fobi.contrib.plugins.form_elements.fields.time',

    # custom metadata form elements
    'fobi_custom.plugins.form_elements.fields.metadata.time_start',
    'fobi_custom.plugins.form_elements.fields.metadata.time_stop',
    'fobi_custom.plugins.form_elements.fields.metadata.time_character',
    'fobi_custom.plugins.form_elements.fields.metadata.representation',
    'fobi_custom.plugins.form_elements.fields.metadata.method',
    'fobi_custom.plugins.form_elements.fields.metadata.microclimate',
    'fobi_custom.plugins.form_elements.fields.metadata.temperature_c',

    # custom intercept form elements
    'fobi_custom.plugins.form_elements.fields.intercept.age_intercept',
    'fobi_custom.plugins.form_elements.fields.intercept.gender_intercept',
    'fobi_custom.plugins.form_elements.fields.intercept.income',
    'fobi_custom.plugins.form_elements.fields.intercept.education',
    'fobi_custom.plugins.form_elements.fields.intercept.race',
    'fobi_custom.plugins.form_elements.fields.intercept.employment',
    'fobi_custom.plugins.form_elements.fields.intercept.household_tenure',
    'fobi_custom.plugins.form_elements.fields.intercept.location_intersection_home',
    'fobi_custom.plugins.form_elements.fields.intercept.location_intersection_work',
    'fobi_custom.plugins.form_elements.fields.intercept.location_zip_home',
    'fobi_custom.plugins.form_elements.fields.intercept.location_zip_work',
    'fobi_custom.plugins.form_elements.fields.intercept.own_or_rent',
    'fobi_custom.plugins.form_elements.fields.intercept.transportation',

    # custom observational form elements
    'fobi_custom.plugins.form_elements.fields.observational.age_observational',
    'fobi_custom.plugins.form_elements.fields.observational.gender_observational',
    'fobi_custom.plugins.form_elements.fields.observational.race_observational',
    'fobi_custom.plugins.form_elements.fields.observational.mode',
    'fobi_custom.plugins.form_elements.fields.observational.groups',
    'fobi_custom.plugins.form_elements.fields.observational.posture',
    'fobi_custom.plugins.form_elements.fields.observational.activity',
    'fobi_custom.plugins.form_elements.fields.observational.objects',

    # fobi form handlers
    'fobi_custom.plugins.form_handlers.collect_data',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'justspaces.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'fobi.context_processors.theme',
            ],
        },
    },
]

WSGI_APPLICATION = 'justspaces.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "users.JustSpacesUser"

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'surveys-list-run'

FOBI_DEFAULT_THEME = 'foundation5'
FOBI_THEME_FOOTER_TEXT = gettext.gettext('')
FOBI_RESTRICT_PLUGIN_ACCESS = False
FOBI_SAVE_SURVEY_REDIRECT_ROUTE = 'surveys-list-edit'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (40, -75.16),  # Centroid of Philadelphia
    'DEFAULT_ZOOM': 11,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'RESET_VIEW': False,
    'TILES': [
        (
         'Map',
         'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
         {'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'}
        ),
        (
         'Satellite',
         'http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}',
         {'attribution': '&copy; Google'}
        ),
    ]
}
