# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.test import TestCase, Client
# from django.contrib.auth.models import User
# from posts.models import Post, Comment
# import datetime

# # Create your tests here.

# class PostTestCase(TestCase):
# 	def setUp(self):
# 		User.objects.create(username='tonystark', email='rdj@stark.com', password='avengers@war')
# 		user = User.objects.first()
# 		Post.objects.create(
# 			user=user,
# 			title='second post',
# 			content = 'this is second post by sunil ',
# 			publish = datetime.datetime.now(),
# 			)

# 		Post.objects.create(
# 			user=user,
# 			title='third post',
# 			content = '',
# 			draft = True,
# 			publish = datetime.datetime.now(),
# 			)
		

# 	def test_post_auto_generate_slug(self):
# 		post1 = Post.objects.get(title__iexact='second post')
# 		post2 = Post.objects.get(title__iexact='third post')
# 		self.assertEqual(post1.slug, 'second-post')
# 		self.assertEqual(post2.slug, 'third-post')

# 	def test_check_draft_post(self):
# 		post2 = Post.objects.get(title__iexact='third post')
# 		self.assertEqual(post2.draft, True)


# class SimpleTest(TestCase):
# 	def setUp(self):
# 		# Every test needs a client 
# 		self.client = Client()
# 		posts = Post.objects.all()

# 	def test_details(self):
# 		# Issue a GET request.
		
# 		response = self.client.get('/posts/list/')

# 		# check that the response is 200 OK.
# 		self.assertEqual(response.status_code, 200)

# 		# check that the rendered context contains 10 posts
		
# 		self.assertEqual(len(response.context_data['posts']), 10)

# 	def test_homeview(self):
# 		response = self.client.get('/posts/list/')
# 		self.assertEqual(response.resolver_match(func=posts.views.HomeView.as_view()),'HomeView')

# 	def test_homepage(self)	:
# 		response = self.client.get('/')
# 		self.assertEqual(response.status_code, 200)