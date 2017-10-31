# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='documents/',
		null = True,
		blank=True,
		width_field="width_field",
		height_field="height_field"
		)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default = False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	read_time = models.IntegerField(default = 0)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		verbose_name_plural = "Posts"
		ordering = ['-publish', '-updated']

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_last_ten_posts(self):
		return self.Post.objects.filter(draft=False)[:10]



def rl_pre_save_receiver(sender, instance, *args, **kwargs):

	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Post)
	



