from .base import *


PROTOCOL = 'http'


# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Staticfiles settings
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')


# Allauth settings
SITE_ID = 3


# Stripe settings
STRIPE_PUBLIC_KEY = 'pk_test_buF4FsDmstqHzKr4Nc5TKxbH00rXE4mpbI'
STRIPE_SECRET_KEY = 'sk_test_bokSwLp3jIVrQ0WYZP4ff8tx009fk1ZPGJ'


# HTML minifier settings
HTML_MINIFY = True


# ReCaptcha V3 settings
os.environ['RECAPTCHA_DISABLE'] = 'True'
