from .base import *

# ----------------------------------------------------
# *** Allowed Hosts ***
# ----------------------------------------------------

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(" ")

# ----------------------------------------------------
# *** Databases ***
# ----------------------------------------------------

DATABASES = {'default': get_env_value('DATABASE_URL')}
# set atomic requests
# DATABASES["default"]["ATOMIC_REQUESTS"] = True

# ----------------------------------------------------
# *** Debug ***
# ----------------------------------------------------

DEBUG = False

# ----------------------------------------------------
# *** Templates ***
# ----------------------------------------------------

TEMPLATES[0]["DIRS"] = [os.path.join(root.path(), "templates")]


# ----------------------------------------------------
# *** LOGGING ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for more details on how to customize logging configuration.

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
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_URL#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True  # Offline compression is required when using Whitenoise
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE_TIMEOUT
COMPRESS_OFFLINE_TIMEOUT = 31536000 # 1 year
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_FILTERS#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
