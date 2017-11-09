# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Post, Comment
import datetime

# Create your tests here.

class PostModelTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		# Set up non-modified objects used by all test methods
		User.objects.create(username='tonystark', email='rdj@stark.com', password='avengers@war')
		user = User.objects.first()
		Post.objects.create(
			user=user,
			title='second post',
			content = 'this is second post by user tonystark ',
			publish = datetime.datetime.now(),
			)

	def test_post_title_label(self):
		post = Post.objects.get(id=1)
		field_label = post._meta.get_field('title').verbose_name
		self.assertEqual(field_label, 'title')

	def test_post_read_time_label(self):
		post = Post.objects.get(id=1)
		field_label = post._meta.get_field('read_time').verbose_name
		self.assertEqual(field_label, 'read time')

	def test_autogenerate_slug(self):
		post = Post.objects.get(id=1)
		self.assertEqual(post.slug, 'second-post')

	def test_title_max_length(self):
		post = Post.objects.get(id=1)
		max_length = post._meta.get_field('title').max_length
		self.assertEqual(max_length, 120)

	def test_get_absolute_url(self):
		post = Post.objects.get(id=1)
		self.assertEqual(post.get_absolute_url(), '/posts/list/1/details/')

	def test_method_get_post_views(self):
		post = Post.objects.get(id=1)
		self.assertEqual(post.views, post.get_post_views())
	