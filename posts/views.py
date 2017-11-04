# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from django.views.generic.edit import (
	FormView,
	CreateView,
	UpdateView, 
	DeleteView
	)
from django.urls import reverse_lazy

from .forms import CommentForm, ContactForm, PostForm
from .models import Post, Comment


# Create your views here.

def home(request):
	posts = Post.objects.filter(draft=False)[:10]

	return render(request, 'home.html', {'posts': posts,})


def posts_list(request):
	posts_list = Post.objects.filter(draft=False)
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


class ContactView(FormView):
	template_name = 'contact.html'
	form_class = ContactForm
	success_url = 'home'

	def form_valid(self, form):
		form.send_email()
		return super(ContactView, self).form_valid(form)

	def form_invalid(self, form):
		return super(ContactView, self).form_invalid(form)
	

class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	context_object_name = 'posts'

	def get_queryset(self):
		queryset = Post.objects.filter(draft=False)[:10]
		return queryset

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['hello_text'] = 'hello there'
		return context


class PostListView(ListView):
	model = Post
	template_name = 'posts/post_list.html'
	context_object_name = 'posts'
	# queryset = Post.objects.filter(draft=False)
	paginate_by = 5

	# def get_context_data(self, **kwargs):
	# 	context = super(PostListView, self).get_context_data(**kwargs)
	# 	context['posts'] = Post.objects.all().order_by('-publish')
	# 	return context

	def get_queryset(self):
		queryset = Post.objects.filter(draft=False)
		q = self.request.GET.get('q')

		if q is not None:
			queryset = Post.objects.filter(
				Q(title__icontains=q),
				Q(draft=False)
				)
			return queryset

		return queryset


	# def post(self, request, *args, **kwargs):
	# 	q = self.request.POST.get('q')
	# 	posts = Post.objects.filter(Q(title__icontains=q))
	# 	return render(request, self.template_name, {'posts': posts})


class PostDetailView(DetailView):
	model = Post
	template_name = 'posts/post_detail.html'
	context_object_name = 'post'
	form_class = CommentForm

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		context['test_title'] = 'hello there'
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		session_key = 'viewed_post_{}'.format(self.object.pk)

		if not request.session.get(session_key, False):
			self.object.views += 1
			self.object.save()
			request.session[session_key] = True
		form = self.form_class()
		return render(request, self.template_name, {'form': form, 'post':self.object})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.form = self.form_class(request.POST)
		parent_id = self.request.GET.get('parent_id')
		
		if self.form.is_valid():
			instance = self.form.save(commit=False)
			instance.user = self.request.user
			instance.post = self.object
			if parent_id is not None:
				parent = get_object_or_404(Comment, pk=parent_id)
				instance.parent = parent
			self.form.save()
		return render(request, self.template_name, {'form': self.form, 'post':self.object})


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'posts/new_post.html'

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.publish = datetime.datetime.now()
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
	permission_required = ('posts.can_change')
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

	# def get_success_message(self):
	# 	return self.success_message('Post Updated Successfully!')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Post
	template_name = 'posts/post_confirm_delete.html'
	success_url = reverse_lazy('posts:list')
	permission_required = ('posts.can_delete')

class CommentUpdateView(UpdateView):
	# model = Comment
	# template_name = 'posts/post_detail.html'
	pass


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



