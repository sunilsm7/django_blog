# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'publish', 'user', 'approved']
	list_filter = ['draft', 'approved']
	date_hierarchy = 'timestamp'
	prepopulated_fields = {"slug": ("title",)}
	list_per_page = 50
	search_fields = ['title', 'content', 'user__username']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'content', 'post']
	list_filter = ['user']
	empty_value_display = '-empty-'
	list_display_links = ('content',)
	#list_editable = ['content',]
	list_per_page = 50
	search_fields = ['post__title','content', 'user__username']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
