import os
from decouple import config
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config('DB_NAME'),
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'digitech/templates'),
            os.path.join(BASE_DIR, 'digitech/templates'),
            os.path.join(BASE_DIR, 'digitech/templates'),
            os.path.join(BASE_DIR, 'digitech/templates'),
            os.path.join(BASE_DIR, 'digitech/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

ADMINS = config('ADMINS')
# ADMINS = [('Isaac', EMAIL_HOST_USER)]
MANAGERS = ADMINS

INSTALLED_APPS = (
    'django.contrib.auth',

    'authtools',
    "geoposition",
    'crispy_forms',
    'easy_thumbnails',
    'captcha',
    'django_countries',

    'digitech.activities',
    'digitech.apply',
    'digitech.authentication',
    'digitech.core',
    'digitech.feeds',
    'digitech.messenger',
    'digitech.search',
    'digitech.operation',
    'rest_framework',
    'phonenumber_field',



    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'user_sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

)
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
SESSION_ENGINE = 'user_sessions.backends.db'
LOGOUT_REDIRECT_URL = '/'
ROOT_URLCONF = 'digitech.urls'
WSGI_APPLICATION = 'digitech.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'live-static', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'digitech/static'),
)
MEDIA_ROOT = os.path.join(BASE_DIR, 'live-static/media')
MEDIA_URL = '/media/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/feeds/'
ALLOWED_SIGNUP_DOMAINS = ['*']
FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0o644
THUMBNAIL_EXTENSION = 'png'
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyCKKERHiiwDU37DQ719Uj93bXVlSGRMn9U'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LfzxiMUAAAAAOx-UBo7PXhP3Apkv3KYsTYkRUBx'
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = '+254'

