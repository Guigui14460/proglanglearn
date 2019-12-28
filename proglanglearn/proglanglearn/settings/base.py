import os

from django.utils.translation import gettext_lazy as _

from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ADMINS = [
    ('Guillaume LETELLIER', 'proglanglearn@gmail.com'),
]

ALLOWED_HOSTS = ['guillaumeletellier.pythonanywhere.com',
                 'proglanglearn.com',
                 '127.0.0.1',
                 ]
INTERNAL_IPS = ('127.0.0.1',)


INSTALLED_APPS = [
    # 'django.contrib.admin',
    'proglanglearn.apps.MyAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',
    'django_countries',
    'filebrowser',
    # 'github',
    'import_export',
    'modeltranslation',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'snowpenguin.django.recaptcha3',
    'tinymce',
    'xhtml2pdf',

    'proglanglearn',
    'accounts',
    'analytics',
    'articles',
    'billing',
    'courses',
    'forum',
    'main',
    'polls',
]

MIDDLEWARE = [
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'proglanglearn.middleware.XForwardedForMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'proglanglearn.middleware.LanguageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Intertionalisation and regionalisation settings
LANGUAGE_CODE = 'fr-Fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fr', _("Français")),
    ('en', _("Anglais"))
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static settings
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')


# Email config
DEFAULT_FROM_EMAIL = 'ProgLangLearn <proglanglearn@gmail.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS')


# Session settings
SESSION_COOKIE_AGE = 3600 * 24 * 7


# Account settings
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
    }
}

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'main:analytics:dashboard'
LOGOUT_REDIRECT_URL = 'main:index'

ACCOUNT_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_LOGOUT_REDIRECT_URL = LOGOUT_REDIRECT_URL

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {
    'login': 'accounts.allauth_forms.LoginForm',
    'signup': 'accounts.allauth_forms.SignupForm',
    'change_password': 'accounts.allauth_forms.ChangePasswordForm',
    'set_password': 'accounts.allauth_forms.SetPasswordForm',
    'reset_password_from_key': 'accounts.allauth_forms.ResetPasswordKeyForm',
}
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True


# Rest-framework settings (API)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}


# TinyMCE settings
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


# Filebrowser settings
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/media_cdn/filebrowser/'
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


# ReCaptcha V3 settings
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.35


# My settings
AUTH_USER_MODEL = 'main.User'
MAX_STRIKE = 3
RESET_LOGIN_AFTER_PASSWORD_RESET = False
SEARCH_TYPE = 'multiple'  # 'simple' or 'multiple'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
CODE_COLOURS_LIST = {
    'android-studio': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/androidstudio.min.css",
    'github': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/github.min.css",
    'monokai': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/monokai.min.css",
    'monokai-sublime': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/monokai-sublime.min.css",
    'vscode': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/vs2015.min.css",
}
CODE_COLOURS = CODE_COLOURS_LIST['vscode']
