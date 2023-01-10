from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'time_create', 'author', 'text', 'status')
    list_display_links = ('id', 'comment')
    search_fields = ('comment', 'text')
    list_editable = ('status',)
    list_filter = ('status', 'time_create')


admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)

