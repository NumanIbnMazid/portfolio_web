from .base import *  # NOQA

# ----------------------------------------------------
# *** Allowed Hosts ***
# ----------------------------------------------------

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(" ")  # NOQA

# ----------------------------------------------------
# *** Databases ***
# ----------------------------------------------------

DATABASES = {'default': get_env_value('DATABASE_URL')}  # NOQA
# set atomic requests
# DATABASES["default"]["ATOMIC_REQUESTS"] = True

# ----------------------------------------------------
# *** Debug ***
# ----------------------------------------------------

DEBUG = False

# ----------------------------------------------------
# *** Templates ***
# ----------------------------------------------------

TEMPLATES[0]["DIRS"] = [os.path.join(root.path(), "templates")]  # NOQA

# ----------------------------------------------------
# *** CACHES ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#caches

CACHES = {
    'default': {
        # https://github.com/django-pymemcache/django-pymemcache
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'rosetta': {
        # https://github.com/django-pymemcache/django-pymemcache
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# ----------------------------------------------------
# *** LOGGING ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for more details
# on how to customize logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


# ----------------------------------------------------
# *** --------------- Third Party --------------- ***
# ----------------------------------------------------

# ----------------------------------------------------
# *** Django Cors Headers ***
# ----------------------------------------------------

CORS_ORIGIN_ALLOW_ALL = True

# ----------------------------------------------------
# *** Django Compressor ***
# ----------------------------------------------------

# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_ENABLED#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)  # NOQA
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_URL#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL  # NOQA
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE
# Offline compression is required when using Whitenoise
COMPRESS_OFFLINE = True
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE_TIMEOUT
COMPRESS_OFFLINE_TIMEOUT = 31536000  # 1 year
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_FILTERS#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}


# ----------------------------------------------------
# *** Django Cleanup (Place to the bottom) ***
# NOTE: Needs to be placed at the bottom of INSTALLED_APPS
# ----------------------------------------------------

if "django_cleanup.apps.CleanupConfig" not in INSTALLED_APPS:  # NOQA
    INSTALLED_APPS.insert(-1, "django_cleanup.apps.CleanupConfig")  # NOQA
