from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns

# third party urls
from config.urls_third_party import urlpatterns as THIRD_PARTY_URL_PATTERNS

# Views
from config.views import HomeView, DashboardView

ADMIN_PANEL_URL_PATTERNS = i18n_patterns(
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("portfolios/", include(("portfolios.urls", "portfolios"), namespace="portfolios")),
    prefix_default_language=False
)

APP_URL_PATTERNS = i18n_patterns(
    path("users/", include(("users.urls", "users"), namespace="users")),
    prefix_default_language=False
) + ADMIN_PANEL_URL_PATTERNS

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False
) + THIRD_PARTY_URL_PATTERNS + APP_URL_PATTERNS

if settings.DEBUG:
    # Static and Media URL
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # This allows the error pages to be debugged during development

    # TODO: active Exception handler URLs and also active htmx redirection from htmx.config.js
    # urlpatterns += [
    #     path(
    #         "400/",
    #         default_views.bad_request,
    #         kwargs={"exception": Exception("Bad Request!")}, name="URL_400",
    #     ),
    #     path(
    #         "403/",
    #         default_views.permission_denied,
    #         kwargs={"exception": Exception("Permission Denied")}, name="URL_403",
    #     ),
    #     path(
    #         "404/",
    #         default_views.page_not_found,
    #         kwargs={"exception": Exception("Page not Found")}, name="URL_404",
    #     ),
    #     path("500/", default_views.server_error, name="URL_500"),
    # ]
