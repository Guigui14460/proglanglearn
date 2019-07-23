import os
from decouple import config
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

ADMINS = [('Guillaume LETELLIER', 'proglanglearn@gmail.com')]

SECRET_KEY = config('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'filebrowser',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third part apps
    'import_export',
    'rest_framework',
    'snowpenguin.django.recaptcha3',
    'tinymce',

    # My apps
    'accounts.apps.AccountsConfig',
    'articles.apps.ArticlesConfig',
    'billing.apps.BillingConfig',
    'courses.apps.CoursesConfig',
    'main.apps.MainConfig',
    'polls.apps.PollsConfig',
]

AUTH_USER_MODEL = 'main.User'

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

CONN_MAX_AGE = 30

WSGI_APPLICATION = 'proglanglearn.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'fr'  # fr-Fr
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
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


# Redirect configs
LOGIN__URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'courses:list'
LOGOUT_REDIRECT_URL = 'main:index'

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS')

# TinyMCE editor config
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': 'auto',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'codesample_languages': [
        {'text': 'Bash', 'value': 'bash'},
        {'text': 'C', 'value': 'c'},
        {'text': 'C#', 'value': 'csharp'},
        {'text': 'C++', 'value': 'cpp'},
        {'text': 'CSS', 'value': 'css'},
        {'text': 'Django Template', 'value': 'django'},
        {'text': 'Go', 'value': 'go'},
        {'text': 'HTML/XML', 'value': 'markup'},
        {'text': 'Java', 'value': 'java'},
        {'text': 'JavaScript', 'value': 'javascript'},
        {'text': 'JSON', 'value': 'json'},
        {'text': 'Julia', 'value': 'julia'},
        {'text': 'Kotlin', 'value': 'kotlin'},
        {'text': 'Markdown', 'value': 'markdown'},
        {'text': 'PHP', 'value': 'php'},
        {'text': 'Plaintext', 'value': 'plaintext'},
        {'text': 'Python', 'value': 'python'},
        {'text': 'Ruby', 'value': 'ruby'},
        {'text': 'Sass/Scss', 'value': 'scss'},
        {'text': 'Swift', 'value': 'swift'},
        {'text': 'TeX/LaTeX', 'value': 'tex'},
    ],
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}
TINYMCE_FILEBROWSER = True

FILEBROWSER_DIRECTORY = 'uploads/'  # tiny_uploads/
DIRECTORY = ''

# ReCaptcha V3 config
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.35

# Filebrowser
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/media_root/filebrowser/'
FILEBROWSER_PATH_FILEBROWSER_MEDIA = BASE_DIR + FILEBROWSER_URL_FILEBROWSER_MEDIA
FILEBROWSER_SHOW_IN_DASHBOARD = False
FILEBROWSER_NORMALIZE_FILENAME = True
FILEBROWSER_LIST_PER_PAGE = 100
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_STATIC_ROOT = STATIC_ROOT
FILEBROWSER_STATIC_URL = STATIC_URL
URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'
URL_TINYMCE = STATIC_URL + 'tinymce/'
PATH_TINYMCE = STATIC_ROOT + 'tinymce/'
