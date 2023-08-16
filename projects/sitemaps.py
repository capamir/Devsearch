from django.contrib.sitemaps import Sitemap
from projects.models import Project


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.created