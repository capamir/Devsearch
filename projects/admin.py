from django.contrib import admin
from .models import Project, Review

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'vote_ratio')
    raw_id_fields = ('owner', 'tags')
    search_fields = ('title', 'description')


class ReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner', 'project')
    list_display = ('project', 'owner', 'value')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Review, ReviewAdmin)
