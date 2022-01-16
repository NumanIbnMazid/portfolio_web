import os
import environ
from django.core.exceptions import ImproperlyConfigured

def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(env_variable)
        raise ImproperlyConfigured(error_msg)

root = environ.Path(__file__) - 3  # get root of the project

# ----------------------------------------------------
# *** Project Environment ***
# ----------------------------------------------------

DEFAULT_ENV_PATH = environ.Path(__file__) - 4
DEFAULT_ENV_FILE = DEFAULT_ENV_PATH.path('.env')()

env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(env.str('ENV_PATH', DEFAULT_ENV_FILE))  # reading .env file

# ----------------------------------------------------
# *** Project's BASE DIRECTORY ***
# ----------------------------------------------------

BASE_DIR = root()

# ----------------------------------------------------
# *** Project's SECRET KEY ***
# ----------------------------------------------------
SECRET_KEY = get_env_value('SECRET_KEY')

# ----------------------------------------------------
# *** Debug Configuration ***
# ----------------------------------------------------

DEBUG = env.bool('DEBUG', default=False)
TEMPLATE_DEBUG = DEBUG

# ----------------------------------------------------
# *** Database Configuration ***
# ----------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR , 'project.db.sqlite3'),
    }
}

# ----------------------------------------------------
# *** Application Definition ***
# ----------------------------------------------------

THIRD_PARTY_APPS = [
    # Django Safe Delete
    "safedelete",
    # Django Crispy Forms
    "crispy_forms",
    "crispy_tailwind",
    # Django Allauth
    "allauth",
    "allauth.account",
    # Django Cleanup (Place to the bottom)
    "django_cleanup.apps.CleanupConfig",
]

LOCAL_APPS = [
    "utils", # for utility management
    "users", # for user management
    "portfolios", # for portfolio management
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # "django.contrib.humanize", # Handy template tags
] + THIRD_PARTY_APPS + LOCAL_APPS

# ----------------------------------------------------
# *** Middleware Definition ***
# ----------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------
# *** Template Definition ***
# ----------------------------------------------------

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
            ],
        },
    },
]

# ----------------------------------------------------
# *** Authentication Definition ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'users.User'

# Django Allauth Authentication Backend
# https://django-allauth.readthedocs.io/en/latest/installation.html
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
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

# ----------------------------------------------------
# *** Email Configuration ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ----------------------------------------------------
# *** Internationalization ***
# ----------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# ----------------------------------------------------
# *** Other Definition ***
# ----------------------------------------------------

SITE_ID = 1
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Session Cookie Age
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # One month
# Default URL's
HOME_URL = "/"
ADMIN_LOGIN_URL = "/accounts/login/"
LOGIN_URL = ADMIN_LOGIN_URL
SITE_DOMAIN = "numanibnmazid.com"

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
# FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
# FIXTURE_DIRS = (os.path.join(BASE_DIR, 'fixtures'),)

# ----------------------------------------------------
# *** Static and Media Files Configuration ***
# ----------------------------------------------------

public_root = root.path('public/')

MEDIA_ROOT = public_root('media')
MEDIA_URL = env.str('MEDIA_URL', default='/media/')

STATIC_ROOT = public_root('static')
STATIC_URL = env.str('STATIC_URL', default='/static/')
STATICFILES_DIRS = [
    os.path.join(public_root, 'staticfiles'),
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# File Upload Configurations
# ----------------------------------------------------
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.svg']
MAX_UPLOAD_SIZE = 2621440 # in bytes (2.62144 MB / 2.5 MB)

# ----------------------------------------------------
# *** SECURITY ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Numan Ibn Mazid""", "numanibnmazid@gmail.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# ----------------------------------------------------
# *** --------------- Third Party --------------- ***
# ----------------------------------------------------

# ----------------------------------------------------
# *** Django WhiteNoise ***
# ----------------------------------------------------

# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

if not "whitenoise.middleware.WhiteNoiseMiddleware" in MIDDLEWARE:
    # Must insert after SecurityMiddleware
    MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1, "whitenoise.middleware.WhiteNoiseMiddleware")

# forever-cacheable files and compression support
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------------------------------
# *** Django Compressor ***
# ----------------------------------------------------

# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation

INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]


# ----------------------------------------------------
# *** Django Cors Headers ***
# ----------------------------------------------------

if not "corsheaders" in INSTALLED_APPS:
    INSTALLED_APPS += ["corsheaders"]

if not "corsheaders.middleware.CorsMiddleware" in MIDDLEWARE:
    MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")


# ----------------------------------------------------
# *** Django Crispy Forms ***
# ----------------------------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_CLASS_CONVERTERS = {
    "textinput": "textinput bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
    "passwordinput": "passwordinput bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
    "dateinput": "dateinput bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
    "urlinput": "urlinput bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
    "textarea": "textarea bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
    "emailinput": "emailinput bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
    "clearablefileinput": "clearablefileinput bg-white dark:bg-gray-700 focus:border-app-theme-400 dark:focus:border-app-theme dark:focus:border-app-theme focus:outline-none focus:shadow-outline-app-theme dark:focus:shadow-outline-app-theme-200 dark:text-white dark:focus:shadow-outline-app-theme form-input",
}


# ----------------------------------------------------
# *** Django Allauth ***
# ----------------------------------------------------

LOGIN_REDIRECT_URL = HOME_URL
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # mandatory, optional, none
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Account Confirmation'
ACCOUNT_FORMS = {
    'login': 'users.forms.CustomLoginForm'
}
