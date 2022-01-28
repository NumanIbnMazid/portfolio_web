# decorator_include imports
from importlib import import_module
from django.urls import URLPattern, URLResolver, include
from django.utils.functional import cached_property

# custom decorator imports
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# ----------------------------------------------------
# *** decorator_include ***
# ----------------------------------------------------


class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """
    def __init__(self, urlconf_module, decorators):
        # ``urlconf_module`` may be:
        #   - an object with an ``urlpatterns`` attribute
        #   - an ``urlpatterns`` itself
        #   - the dotted Python path to a module with an ``urlpatters`` attribute
        self.urlconf = urlconf_module
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators

    def decorate_pattern(self, pattern):
        if isinstance(pattern, URLResolver):
            decorated = URLResolver(
                pattern.pattern,
                DecoratedPatterns(pattern.urlconf_module, self.decorators),
                pattern.default_kwargs,
                pattern.app_name,
                pattern.namespace,
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = URLPattern(
                pattern.pattern,
                callback,
                pattern.default_args,
                pattern.name,
            )
        return decorated

    @cached_property
    def urlpatterns(self):
        # urlconf_module might be a valid set of patterns, so we default to it.
        patterns = getattr(self.urlconf_module, 'urlpatterns', self.urlconf_module)
        return [self.decorate_pattern(pattern) for pattern in patterns]

    @cached_property
    def urlconf_module(self):
        if isinstance(self.urlconf, str):
            return import_module(self.urlconf)
        else:
            return self.urlconf

    @cached_property
    def app_name(self):
        return getattr(self.urlconf_module, 'app_name', None)


def decorator_include(decorators, arg, namespace=None):
    """
    Works like ``django.conf.urls.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    if isinstance(arg, tuple) and len(arg) == 3 and not isinstance(arg[0], str):
        # Special case where the function is used for something like `admin.site.urls`, which
        # returns a tuple with the object containing the urls, the app name, and the namespace
        # `include` does not support this pattern (you pass directly `admin.site.urls`, without
        # using `include`) but we have to
        urlconf_module, app_name, namespace = arg
    else:
        urlconf_module, app_name, namespace = include(arg, namespace=namespace)
    return DecoratedPatterns(urlconf_module, decorators), app_name, namespace


# ----------------------------------------------------
# *** is_superuser_required ***
# ----------------------------------------------------


is_superuser = user_passes_test(
    lambda user: user.is_superuser is True, login_url=settings.DECORATOR_REDIRECT_URL
)


def is_superuser_required(view_func):
    decorated_view_func = login_required(is_superuser(view_func))
    return decorated_view_func


# ----------------------------------------------------
# *** is_staff_required ***
# ----------------------------------------------------


is_staff = user_passes_test(
    lambda user: user.is_staff is True, login_url=settings.DECORATOR_REDIRECT_URL
)


def is_staff_required(view_func):
    decorated_view_func = login_required(is_staff(view_func))
    return decorated_view_func
