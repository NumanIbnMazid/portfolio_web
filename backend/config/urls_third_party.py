from django.urls import path, include, re_path
from django.conf import settings
from utils.decorators import decorator_include, is_superuser_required

urlpatterns = [
    # Third Party URL Patterns

    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
]

# Rosetta URL Patterns
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^translations/', decorator_include([is_superuser_required], include('rosetta.urls'), namespace='rosetta')),
    ]

if settings.DEBUG:
    # Django Debug Toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
