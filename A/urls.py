from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

from django.conf import settings
from django.conf.urls.static import static

from projects.sitemaps import ProjectSitemap
from projects.models import Project

# sitemaps = {
#     "project": ProjectSitemap,
# }
project_info_dict = {
    "queryset": Project.objects.all(),
    "date_field": "created",
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls', namespace='projects')),
    path('', include('accounts.urls', namespace='accounts')),

    # path(
    #     "sitemap.xml",
    #     sitemap,
    #     {"sitemaps": sitemaps},
    #     name="django.contrib.sitemaps.views.sitemap",
    # ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"project": GenericSitemap(project_info_dict, priority=0.6)}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
