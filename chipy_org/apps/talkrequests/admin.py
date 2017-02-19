from django.contrib import admin
from . import models


class TalkRequestAdmin(admin.ModelAdmin):
    list_display = [
        'submitter', 'title', 'active',
        'category', 'created', 'modified', 'recent_date']
    search_fields = ['title', 'text', 'id']
    list_filter = ['active']


class TalkCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'created', 'modified']
    search_fields = ['name', 'slug', 'id']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.TalkRequest, TalkRequestAdmin)
admin.site.register(models.TalkCategory, TalkCategoryAdmin)
