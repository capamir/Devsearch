from django.contrib import admin
from .models import Profile, Skill

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('username', 'email', 'location',)
    search_fields = ('username', 'email', 'name')


class SkillAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)
    list_display = ('owner', 'name')
    search_fields = ('name',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
