from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'published_date', 'created_at']
    list_filter = ['category', 'is_published', 'published_date']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_date']
    date_hierarchy = 'published_date'