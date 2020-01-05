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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'init_command': 'SET default_storage_engine=INNODB',
#             'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
#             'NAME': 'guillaumeletelli$ProgLangLearn',
#             'USER': 'guillaumeletelli',
#             'PASSWORD': '9,:bkCJx{(mRbSLgcbs?`-BM@6y*XT,w.\+%zZXyqY',
#             'HOST': 'guillaumeletellier.mysql.pythonanywhere-services.com',
#             'PORT': 9999,
#         },
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Staticfiles settings
STATIC_ROOT = '/home/guillaumeletellier/proglanglearn/proglanglearn/static_cdn'
MEDIA_ROOT = '/home/guillaumeletellier/proglanglearn/proglanglearn/media_cdn'


# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.4,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 16,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Session settings
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_SECURE = True


# Allauth settings
SITE_ID = 4


# Stripe settings
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
