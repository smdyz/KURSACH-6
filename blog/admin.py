from django.contrib import admin

from blog.models import Blog


# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'views_count', 'is_published', 'publish_date')
    search_fields = ('id', 'title', 'body', 'publish_date')
    list_filter = ('title', 'is_published',)