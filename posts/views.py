# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import django_filters
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Q, F, Count, ExpressionWrapper, IntegerField
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import (
	FormView,
	CreateView,
	UpdateView, 
	DeleteView
	)
from django.urls import reverse_lazy
from django.utils.html import mark_safe
from markdown import markdown

from .api.permissions import IsOwnerOrReadOnly
from .forms import CommentForm, ContactForm, PostForm
from .mixins import AjaxFormMixin
from .models import Post, Comment


# Create your views here.

def home(request):
	posts = Post.objects.published()[:10]
	return render(request, 'home.html', {'posts': posts,})


def posts_list(request):
	posts_list = Post.objects.published()
	page = request.GET.get('page', 1)
	paginator = Paginator(posts_list, 10)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
		
	return render(request, 'posts/post_list.html', {'posts': posts})


def post_details(request, pk):
	post = get_object_or_404(Post, pk=pk)
	session_key = 'viewed_post_{}'.format(post.pk)
	
	if not request.session.get(session_key, False):
		post.views += 1
		post.save()
		request.session[session_key] = True

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.post = post
			form.save()
			return redirect('posts:details', pk=post.pk)
	else:
		form = CommentForm()

	return render(request, 'posts/post_detail.html', {'post': post, 'form':form})


@login_required
def new_post(request):
	title_text = 'New Post'
	
	if request.method == 'POST':
		form = PostForm(request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.publish = datetime.datetime.now()
			form.save()
			return redirect('home')
	else:
		form = PostForm()
	return render(request, 'posts/new_post.html', {'form': form, 'title_text':title_text})


@login_required
def edit_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	title_text = 'Edit Post'

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.publish = datetime.datetime.now()
			obj = form.save()
			messages.success(request, 'Post Updated Successfully!')
			return redirect('posts:details', pk=obj.pk)
		else:
			messages.warning(request, 'Please correct the error below.')
	else:
		form = PostForm(instance=post)

	return render(request, 'posts/new_post.html', {'form': form, 'title_text': title_text})


def delete_post(request, pk):
	instance = get_object_or_404(Post, pk=pk)
	instance.delete()
	messages.success(request, 'Post: {} Deleted Succussfully!'.format(instance.title))
	return redirect('posts:list')


class ContactView(AjaxFormMixin, FormView):
	template_name = 'contact.html'
	form_class = ContactForm
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		response = super(ContactView, self).form_valid(form)
		if self.request.is_ajax():
			name = form.cleaned_data['name']
			subject = form.cleaned_data['subject']
			email = form.cleaned_data['email']
			message = form.cleaned_data['message']
			marked_message = mark_safe(markdown(message, safe_mode='escape'))
			send_mail(subject, marked_message, email, ['admin@example.com'])
			data = {
				'message': 'Successfully send data. We will revert soon.'
			}
			return JsonResponse(data)
		else:
			return response

	def form_invalid(self, form):
		response = super(ContactView, self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response


class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		queryset = Post.objects.published()
		return queryset


class PostListView(ListView):
	model = Post
	template_name = 'posts/post_list.html'
	context_object_name = 'posts'
	# queryset = Post.objects.filter(draft=False)
	paginate_by = 10

	def get_queryset(self):
		queryset = Post.objects.published()
		q = self.request.GET.get('q')
		if q is not None:
			queryset = queryset.search(q)
			return queryset
		return queryset


class PostDetailView(DetailView):
	model = Post
	template_name = 'posts/post_detail.html'
	context_object_name = 'post'
	form_class = CommentForm

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		context['modal_title'] = 'Comment Reply'
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		session_key = 'viewed_post_{}'.format(self.object.pk)

		if not request.session.get(session_key, False):
			# self.object.views += 1
			self.object.views = ExpressionWrapper(F('views') + 1, output_field=IntegerField)
			self.object.save()
			request.session[session_key] = True
		form = self.form_class()
		post_comments = self.object.get_comments
		return render(request, self.template_name, {'form': form, 'post':self.object, 'post_comments':post_comments})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.form = self.form_class(request.POST)
		data = dict()
		if request.is_ajax():	
			try:
				parent_id = self.request.POST.get('parent')
			except:
				parent_id = None
			
			if self.form.is_valid():
				instance = self.form.save(commit=False)
				instance.user = self.request.user
				instance.post = self.object
				
				if parent_id is not None:
					parent = get_object_or_404(Comment, pk=parent_id)
					instance.parent = parent
					self.form.save()
				objects = self.form.save()
				data['message'] = 'success'
				return JsonResponse(data, safe=False)
			else:
				data['message'] = 'errors'
				return JsonResponse(data)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	login_url = 'profiles:login'
	template_name = 'posts/new_post.html'
	permission_required = ('posts.add_post')

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.publish = datetime.datetime.now()
		instance.save()
		return super(PostCreateView, self).form_valid(form)
		
	def form_invalid(self, form):
		return super(PostCreateView, self).form_invalid(form)
		
	def get_context_data(self, **kwargs):
		context = super(PostCreateView, self).get_context_data(**kwargs)
		context['title_text'] = 'New Post'
		context['btn_text'] = 'Create Post'
		return context 


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm
	permission_required = ('posts.change_post')
	template_name = 'posts/new_post.html'
	# success_url = reverse_lazy('posts:list')
	success_message = "Post updated successfully"

	def get_success_url(self):
		self.object = self.get_object()
		return reverse_lazy('posts:details', args=[self.object.id])

	def get_context_data(self, **kwargs):
		context = super(PostUpdateView, self).get_context_data(**kwargs)
		context['title_text'] = 'Edit Post'
		context['btn_text'] = 'Update Post'
		return context


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Post
	template_name = 'posts/post_confirm_delete.html'
	success_url = reverse_lazy('posts:list')
	permission_required = ('posts.delete_post')


class RepliesListView(ListView):
	model = Comment
	template_name = 'posts/comment_replies.html'
	context_object_name = 'replies'
	paginate_by = 10

	def get_queryset(self, *args,**kwargs):
		comment_id = self.kwargs['comment_pk']
		queryset = Comment.objects.filter(parent=comment_id)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(RepliesListView, self).get_context_data(**kwargs)
		comment_id = self.kwargs['comment_pk']
		context['comment'] = get_object_or_404(Comment, id=comment_id)
		context['post_id'] = self.kwargs['pk']
		return context 


def get_posts(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		queryset = Post.objects.published()
		posts = queryset.filter(title__icontains=q)
		results = []
		for post in posts:
			post_json = {}
			post_json['id'] = post.id
			post_json['label'] = post.title
			post_json['value'] = post.title
			results.append(post_json)
		data_json = json.dumps(results)
	else:
		data_json = 'fail'
	return HttpResponse(data_json, content_type='application/json')