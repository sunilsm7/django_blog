# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'publish', 'user']
	list_filter = ['user']
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
