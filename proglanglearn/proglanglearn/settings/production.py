import os

from .base import *


PROTOCOL = 'https'


# Database settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': 9999,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Staticfiles settings
# STATIC_ROOT = '/home/guillaumeletellier/proglanglearn/static_cdn'
# MEDIA_ROOT = '/home/guillaumeletellier/proglanglearn/media_cdn'


# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Allauth settings
SITE_ID = 4


# Stripe settings
# STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
# STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = 'pk_test_buF4FsDmstqHzKr4Nc5TKxbH00rXE4mpbI'
STRIPE_SECRET_KEY = 'sk_test_bokSwLp3jIVrQ0WYZP4ff8tx009fk1ZPGJ'
