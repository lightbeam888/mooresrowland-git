from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from wagtail.documents import urls as wagtaildocs_urls
from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.views.generic import TemplateView
from wagtail.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # Admin
    path('sitemap.xml', sitemap),
    path("test_404/", TemplateView.as_view(template_name="404.html")),
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    path('login/', LoginView.as_view(template_name='coderedcms/pages/login.html'), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns = urlpatterns + i18n_patterns(
    # Search
    path("search/", include(crx_search_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(crx_urls)),
    # Alternatively, if you want pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(crx_urls)),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
