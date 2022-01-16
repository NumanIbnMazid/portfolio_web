from django.urls import path, include
from django.conf import settings

urlpatterns = [
    # Third Party URL Patterns

    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    # Django Debug Toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
