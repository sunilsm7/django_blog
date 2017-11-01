# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'publish', 'user']
	list_filter = ['user']
	prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'post', 'content']
	list_filter = ['user', 'post']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
