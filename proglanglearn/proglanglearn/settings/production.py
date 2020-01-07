import os

from .base import *


PROTOCOL = 'https'


# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'proglanglearn-database-1',
        'USER': 'pll_master',
        'PASSWORD': 'kN9jutdGK85cn2MLthrp2zrcry2bQrG9CfXbndKTF6gPNW8X32dp8Na2xRr9Z8ygCvHPV6afKWF',
        'HOST': 'proglanglearn-database-1.cahphcqcqndw.eu-west-3.rds.amazonaws.com',
        'PORT': 5432,
    }
}
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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Staticfiles settings
# STATIC_ROOT = '/home/guillaumeletellier/proglanglearn/proglanglearn/static_cdn'
# MEDIA_ROOT = '/home/guillaumeletellier/proglanglearn/proglanglearn/media_cdn'
STATIC_ROOT = '/home/ubuntu/pll_root/proglanglearn/static_cdn'
MEDIA_ROOT = '/home/ubuntu/pll_root/proglanglearn/media_cdn'



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
SESSION_COOKIE_SECURE = True


# Security settings
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Filebrowser settings
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_STATIC_ROOT = STATIC_ROOT
FILEBROWSER_STATIC_URL = STATIC_URL
URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'
URL_TINYMCE = STATIC_URL + 'tinymce/'
PATH_TINYMCE = STATIC_ROOT + 'tinymce/'


# Allauth settings
#SITE_ID = 4
SITE_ID = 1
USE_X_FORWARDED_HOST = True


# Stripe settings
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
