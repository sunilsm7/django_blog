# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from accounts.models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'activated', 'timestamp', 'updated']
	list_filter = ['activated']
	search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)