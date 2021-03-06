from django import template
from django.contrib.auth.models import User, Group
from django.db.models import Q, Count
from posts.models import Post

import datetime

register = template.Library()

# @register.simple_tag
# def current_time():
#     return datetime.datetime.now()

@register.inclusion_tag('posts/includes/custom_tags_posts_list.html')
def latest_updated_posts():
	posts_list = Post.objects.published().order_by('-updated')[:5]
	return {'posts_list': posts_list}


@register.inclusion_tag('posts/includes/custom_tags_posts_list.html')
def most_viewd_posts():
	posts_list = Post.objects.published().order_by('-views')[:5]
	return {'posts_list': posts_list}


@register.inclusion_tag('posts/includes/custom_tags_posts_list.html')
def most_commented_posts():
	posts_objects = Post.objects.annotate(num_comments=Count('comments'))
	posts_list = posts_objects.order_by('-num_comments')[:5]
	return {'posts_list':posts_list}


@register.inclusion_tag('posts/includes/posts_count_by_user_list.html')
def most_posts_by_user():
	posts_objects = User.objects.annotate(num_posts=Count('posts'))
	user_list = posts_objects.order_by('-num_posts')[:5]
	return {'user_list':user_list}


@register.filter(name='has_group')
def has_group(user, group_name):
	group = Group.objects.get(name=group_name)
	return True if group in user.groups.all() else False