from django.contrib.auth.models import User, Permission
from django.test import TestCase

from posts.models import Post

from django.urls import reverse_lazy
import datetime

class PostListViewTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		# create 13 posts for pagination tests
		User.objects.create_user(username='tonystark', email='rdj@stark.com', password='avengers@war')
		user = User.objects.first()
		num_of_posts = 13
		for num_of_post in range(num_of_posts):
			Post.objects.create(
				user = user,
				title='test title #{}'.format(num_of_post), 
				content='test title description #{}'.format(num_of_post), 
				publish=datetime.datetime.now(),
				)

	def test_post_list_view_status_code_200(self):
		response = self.client.get('/posts/list/')
		self.assertEqual(response.status_code, 200)

	def test_post_list_view_template_name_correct(self):
		response = self.client.get(reverse_lazy('posts:list'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'posts/post_list.html')

	def test_post_list_pagination_is_ten(self):
		response = self.client.get(reverse_lazy('posts:list'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertEqual(len(response.context['posts']), 10)

	def test_post_list_all_posts(self):
		# get second page and confirm it has remaining 3 posts
		response = self.client.get(reverse_lazy('posts:list')+'?page=2')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertTrue(len(response.context['posts']) == 3)


class PostCreateViewTest(TestCase):
	def setUp(self):
		test1_user = User.objects.create_user(username='tonystark', email='rdj@stark.com', password='avengers@ironman')
		test1_user.save()
		test2_user = User.objects.create_user(username='brucebanner', email='incredible_hulk@stark.com', password='strognestavenger')
		test2_user.save()

		user1 = User.objects.first()
		user2 = User.objects.last()		
		num_of_posts = 13
		for num_of_post in range(num_of_posts):
			Post.objects.create(
				user = user1,
				title='test title #{}'.format(num_of_post), 
				content='test title description #{}'.format(num_of_post), 
				publish=datetime.datetime.now(),
				)

	def test_redirect_if_not_logged_in(self):
		response = self.client.get(reverse_lazy('posts:new-post'))
		self.assertRedirects(response, '/accounts/login/?next=/posts/list/new-post/')

	def test_logged_in_uses_correct_template(self):
		login = self.client.login(username='tonystark', password='avengers@ironman')
		self.assertTrue(login)

		response = self.client.get(reverse_lazy('posts:new-post'))
		
		# check our user is logged in
		self.assertEqual(str(response.context['user']), 'tonystark')
		# check that we got a response success
		self.assertEqual(response.status_code, 200)

		# check we used correct template
		self.assertTemplateUsed(response, 'posts/new_post.html')

	def test_posts_by_user(self):
		login = self.client.login(username='tonystark', password='avengers@ironman')
		url = reverse_lazy('accounts:profile')
		response = self.client.get(url)
		# check user is logged in
		self.assertEqual(str(response.context['user']), 'tonystark')
		#check that we got a response success
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['user_posts']), 10)


class PostUpdateView(TestCase):

	def setUp(self):
		permission = Permission.objects.get(name='Can change post')
		
		# create user
		test1_user = User.objects.create_user(username='tonystark', email='rdj@stark.com', password='avengers@ironman')
		test1_user.save()
		test2_user = User.objects.create_user(username='brucebanner', email='incredible_hulk@stark.com', password='strognestavenger')
		test2_user.user_permissions.add(permission)
		test2_user.save()

		test3_user = User.objects.create_user(username='thor', email='thor@stark.com', password='godofthunder')
		test3_user.user_permissions.add(permission)
		test3_user.save()
		
		self.test_post1 = Post.objects.create(
			user=test1_user,
			title='ironman post',
			content = 'this is second post by user tonystark ',
			publish = datetime.datetime.now(),
			)
		self.test_post1.save()

		self.test_post2 = Post.objects.create(
			user=test2_user,
			title='incredible_hulk post',
			content = 'this is second post by user brucebanner ',
			publish = datetime.datetime.now(),
			)
		self.test_post2.save()

		self.test_post3 = Post.objects.create(
			user=test3_user,
			title='God of Thunder post',
			content = 'post by user thor ',
			publish = datetime.datetime.now(),
			)
		self.test_post3.save()

	def test_redirect_if_not_logged_in(self):
		response = self.client.get(reverse_lazy('posts:edit', kwargs={'pk':self.test_post1.pk }))
		self.assertEqual(response.status_code, 302)
		self.assertTrue(response.url.startswith('/accounts/login/'))

	def test_redirect_if_logged_in_but_not_correct_permission(self):
		login = self.client.login(username='tonystark', password='avengers@ironman')
		self.assertTrue(login)
		response = self.client.get(reverse_lazy('posts:edit', kwargs={'pk':self.test_post1.pk }))
		self.assertEqual(response.status_code, 302)
		self.assertTrue(response.url.startswith('/accounts/login/'))

	def test_logged_in_with_permission_edit_post(self):
		login = self.client.login(username='brucebanner', password='strognestavenger')
		
		self.assertTrue(login)
		response = self.client.get(reverse_lazy('posts:edit', kwargs={'pk':self.test_post2.pk }))
		self.assertTrue(response.url.startswith('/accounts/login/'))
		#self.assertEqual(response.status_code, 200)

	def test_logged_in_other_users_edit_post(self):
		login = self.client.login(username='brucebanner', password='strognestavenger')
		self.assertTrue(login)
		response = self.client.get(reverse_lazy('posts:edit', kwargs={'pk':self.test_post3.pk }))
		self.assertTrue(response.url.startswith('/accounts/login/'))
		self.assertEqual(response.status_code, 302)

	def test_HTTP404_for_invalid_post_if_logged_in(self):
		login = self.client.login(username='thor', password='godofthunder')
		self.assertTrue(login)
		url = ('/posts/list/260/')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)