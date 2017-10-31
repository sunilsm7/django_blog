# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post
from .forms import NewPostForm,PostForm
import datetime
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
	return render(request, 'posts/post_detail.html', {'post': post})


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
	
