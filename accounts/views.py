# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.html import mark_safe
from markdown import markdown

from .forms import SignUpForm, WriteForUsForm
from pinax.messages.models import Message
from posts.models import Post
from .utils import account_activation_token

# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html', {'form':form })


class SignUpView(FormView):
	template_name = 'registration/signup.html'
	form_class = SignUpForm
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		subject = 'Activate Your Django Unchained Account'
		message = render_to_string('accounts/email_snippets/account_activation_email.html', {
			'user' : user,
			'domain' : current_site.domain,
			'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
			'activation_key' : account_activation_token.make_token(user),
			})
		user.email_user(subject, message)
		return redirect('accounts:account_activation_sent')
		# auth_login(self.request, user)
		# return super(SignUpView, self).form_valid(form)

	def form_invalid(self, form):
		return super(SignUpView, self).form_invalid(form)


def account_activation_sent(request):
	return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, activation_key):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, activation_key):
		user.is_active = True
		user.profile.activated = True
		user.save()
		auth_login(request, user)
		return redirect('home')
	else:
		return render(request, 'accounts/account_activation_invalid.html')


class DashboardView(View):
	model = User
	template_name = 'accounts/dashboard.html'
	context_object_name = 'user_posts'
	paginate_by = 10
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'user_posts': self.context_object_name})


def validate_username(request):
	if request.is_ajax:
		username = request.GET.get('username', None)
		email = request.GET.get('email', None)
		users = User.objects.all()
		data = {
			'username_is_taken' : users.filter(username__iexact=username).exists(),
			'email_is_taken' : users.filter(email__iexact=email).exists()
		}
		if data['username_is_taken']:
			data['username_error_message'] = 'A user with this username already exists.'
		elif data['email_is_taken']:
			data['email_error_message'] = 'You can not use this email id.'
		return JsonResponse(data)


class PostListView(ListView):
	model = Post
	template_name = 'accounts/post_list.html'
	context_object_name = 'posts'
	paginate_by = 20

	def get_queryset(self):
		queryset = Post.objects.all()
		return queryset


def mail_to_user_template(template_name, user, email, subject, current_site): 
	message = render_to_string(template_name, {
		'user': user,
		'email': email,
		'domain':current_site,
		})
	sent_mail = send_mail(subject, message, 'admin@example.com', [email, ],)
	return sent_mail


@login_required
def add_remove_author(request):
	if request.is_ajax:
		username = request.POST.get('username')
		check_status = request.POST.get('author_status');
		author_group = Group.objects.get(name='Authors')
		current_site = get_current_site(request)

		try:
			user = get_object_or_404(User, username=username)
		except:
			pass

		author_qs = author_group.user_set.filter(username=username)
		
		if author_qs.exists():
			author_group.user_set.remove(user)
			template_name = 'accounts/email_snippets/author_approval_rejection_email.html'
			subject = "Author Permission Removed"
			email = user.email
			content = "Your Author permission has been removed"
			Message.new_message(from_user=request.user, to_users=[user], subject=subject, content=content)
			mail_to_user_template(template_name, user, email, subject, current_site)
			data = {
				'username':username,
				'author': 'False'
			}
			return JsonResponse(data)
		else:
			author_group.user_set.add(user)
			template_name = 'accounts/email_snippets/author_approval_email.html'
			subject = "Author Permission Granted"
			email = user.email
			content = "Congratulations, Author Permission Granted"
			Message.new_message(from_user=request.user, to_users=[user], subject=subject, content=content)
			mail_to_user_template(template_name, user, email, subject, current_site)
			data = {
				'username':username,
				'author': 'True'
			}
			return JsonResponse(data)


@login_required
def write_for_us(request):
	context = {}
	if request.method == 'POST':
		form = WriteForUsForm(request.POST)
		if form.is_valid():
			user = request.user
			admin_user = User.objects.get(username='admin')
			email = user.email
			subject = 'Write for us'
			user_message = form.cleaned_data['message']
			# user_message = mark_safe(markdown(user_message, safe_mode='escape'))
			message = render_to_string('accounts/email_snippets/write_for_us_email.html', {
				'user': user,
				'email': email,
				'message' : user_message,
				})
			send_mail(subject, message, email, ['admin@example.com'])
			
			messages.success(request, 'Request Send Successfully!.')
			content = "thank you for showing interest to write with us. we\'ll revert soon."
			Message.new_message(from_user=admin_user, to_users=[user], subject=subject, content=content)
			form = WriteForUsForm()
			return render(request, 'accounts/write_for_us.html', context={'form':form})
	else:
		form = WriteForUsForm()
	context['form'] = form
	return render(request, 'accounts/write_for_us.html', context=context)


@login_required
def post_approved_change(request):
	current_site = None

	if request.is_ajax:
		post_id = request.POST.get('post_id')
		approved = request.POST.get('approved')
		post = get_object_or_404(Post, id=post_id)
		user = post.user 
		post.approved = approved
		post.save()

		approved_status = post.approved
		current_site = get_current_site(request)
		subject = 'Post Approval'
		email = user.email
		message = render_to_string('accounts/email_snippets/post_approved_email.html', {
			'user': user,
			'email': email,
			'post' : post,
			'domain':current_site,
			})
		
		send_mail(subject, message, 'admin@example.com', [email, ],)

		if approved_status == 'True':
			content = "the post {title} has been approved.".format(title=post.title)
			Message.new_message(from_user=request.user, to_users=[user], subject=subject, content=content)
		else:
			content = "the post {title} has not approved.".format(title=post.title)
			Message.new_message(from_user=request.user, to_users=[user], subject=subject, content=content)
		data = {
			'post_id':post_id,
			'approved':approved_status
		}
		return JsonResponse(data)