# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Q, F, Count
from django.db.models.signals import pre_save, post_save
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.utils.html import mark_safe
from markdown import markdown

from .managers import PostManager
from .utils import unique_slug_generator
# Create your models here.


class Post(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'posts', default=1)
	title 			= models.CharField(max_length=120)
	slug 			= models.SlugField(unique=True)
	image 			= models.ImageField(upload_to='media/',
		null = True,
		blank=True,
		width_field="width_field",
		height_field="height_field"
		)
	height_field 	= models.IntegerField(default=0)
	width_field 	= models.IntegerField(default=0)
	content 		= models.TextField()
	draft 			= models.BooleanField(default = False)
	approved 		= models.BooleanField(default = False)
	publish 		= models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
	read_time 		= models.IntegerField(default = 0)
	views 			= models.PositiveIntegerField(default=0)
	updated 		= models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp 		= models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()
	# objects  = models.Manager()

	class Meta:
		verbose_name_plural = "01 Posts"
		ordering = ['-timestamp',]

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_content_as_markdown(self):
		return mark_safe(markdown(self.content, safe_mode='escape'))

	def get_absolute_url(self):
		return reverse_lazy('posts:details', args=[str(self.id)])

	def get_post_views(self):
		return self.views


	@property
	def get_comments(self):
		instance = self
		qs = Comment.objects.filter(post=instance)
		return qs



class Comment(models.Model):
	user 	= models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	post 	= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	parent 	= models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name_plural = '02 Comments'
		ordering = ['-timestamp']

	# def get_parent_comment(self):
	# 	return Comment.objects.filter(parent=self.parent)

	def __str__(self):
		return '{} {}'.format(self.user, self.content, self.parent)

	def __unicode__(self):
		return '{} {}'.format(self.user, self.content, self.parent)

	# def get_absolute_url(self):
	# 	return reverse_lazy('posts:replies', args=[str(self.post.id), str(self.id)])

	def get_content_as_markdown(self):
		return mark_safe(markdown(self.content, safe_mode='escape'))

	def has_replies(self):
		return Comment.objects.filter(parent=self)


def rl_pre_save_receiver(sender, instance, *args, **kwargs):

	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Post)
	



