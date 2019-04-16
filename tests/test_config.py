import os
import gettext

SECRET_KEY = 'a truly secret test key'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'just-spaces',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'users',
    'frontend',
    'surveys',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',

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

    # custom PLDP form elements
    'fobi_custom.plugins.form_elements.fields.age',
    'fobi_custom.plugins.form_elements.fields.gender',
    'fobi_custom.plugins.form_elements.fields.study',
    # 'fobi_custom.plugins.form_elements.fields.time_start',
    # 'fobi_custom.plugins.form_elements.fields.time_stop',
    'fobi_custom.plugins.form_elements.fields.survey_representation',
    'fobi_custom.plugins.form_elements.fields.survey_method',

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

TIME_ZONE = 'UTC'

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
