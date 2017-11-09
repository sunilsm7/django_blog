from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy, resolve

from posts.forms import PostForm
from posts.models import Post, Comment
from posts.views import PostCreateView
import datetime

class NewPostFormTest(TestCase):
	def setUp(self):
		User.objects.create_user(username='tonystark', email='rdj@stark.com', password='avengers@war')
		user = User.objects.first()
		# Post.objects.create(
		# 	user=user,
		# 	title='second post',
		# 	content = 'this is second post by user tonystark ',
		# 	publish = datetime.datetime.now(),
		# 	)
		self.client.login(username='tonystark', password='avengers@war')

	def test_new_post_view_success_status_code(self):
		url = reverse_lazy('posts:new-post')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_new_post_url_resolves_new_post_view(self):
		view = resolve('/posts/list/new-post/')
		self.assertEqual(view.func.view_class, PostCreateView)

	def test_new_post_view_contains_link_back_to_home(self):
		url = reverse_lazy('posts:new-post')
		home_url = reverse_lazy('home')
		response = self.client.get(url)
		self.assertContains(response, 'href="{0}"'.format(home_url))

	def test_csrf(self):
		url = reverse_lazy('posts:new-post')
		response =self.client.get(url)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		url = reverse_lazy('posts:new-post')
		response = self.client.get(url)
		form = response.context.get('form')
		self.assertIsInstance(form, PostForm)

	def test_new_post_valid_data(self):
		url = reverse_lazy('posts:new-post')
		data = {
			'title' : 'Test title',
			'content': 'Lorem ipsum dolor, sit amet',
			'read_time': 5,
		}
		self.client.post(url, data)
		self.assertTrue(Post.objects.exists())

	def test_new_post_invalid_post_data(self):
		url = reverse_lazy('posts:new-post')
		data = {
			'title' : '',
			'content': 'Lorem ipsum dolor, sit amet',
			'read_time': '',
		}
		response = self.client.post(url, {})
		form = response.context.get('form')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(form.errors)

	def test_new_post_invalid_post_data_with_empty_fields(self):
		url = reverse_lazy('posts:new-post')
		data = {
			'title' : '',
			'content': '',
			'read_time': '',
		}
		response = self.client.post(url, data)
		form = response.context.get('form')
		self.assertFalse(Post.objects.exists())
		self.assertEqual(response.status_code, 200)
		self.assertTrue(form.errors)

	def test_postform_title_field_label(self):
		form = PostForm()
		self.assertTrue(form.fields['title'].label == None or form.fields['title'].label == 'Title')



