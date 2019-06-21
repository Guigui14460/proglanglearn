import os
from decouple import config
from django.utils.translation import gettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

ADMINS = [('Guillaume LETELLIER', 'proglanglearn@gmail.com')]

SECRET_KEY = config('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third part apps
    'ckeditor',
    'ckeditor_uploader',
    'import_export',
    'snowpenguin.django.recaptcha3',

    # My apps
    'main.apps.MainConfig',
    'accounts.apps.AccountsConfig',
    'courses.apps.CoursesConfig',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    # HTML minifer
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proglanglearn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'proglanglearn.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'fr-Fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fr', _("Français")),
    ('en', _("Anglais"))
]

# Static files (CSS, JavaScript, Images, ...)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Redirect configs
LOGIN__URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'main:index'
LOGOUT_REDIRECT_URL = 'main:index'

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS')

# CKEditor config
CKEDITOR_JQUERY_URL = 'https://code.jquery.com/jquery-3.4.1.min.js'
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
        'height': '250px',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline',
                'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source', 'CodeSnippet'],
        ],
    },
    'blog': {
        'toolbar': 'Blog',
        'toolbar_Blog': [
            ['Bold', 'Link', 'Source', 'CodeSnippet', 'Youtube', 'Mathjax']
        ],
        'extraPlugins': ','.join(['codesnippet', 'youtube', 'mathjax'])
    }
}

# ReCaptcha V3 config
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.35
