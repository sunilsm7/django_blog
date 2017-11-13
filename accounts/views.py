# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from django.views import View
from django.views.generic.edit import FormView

from .forms import SignUpForm
# from posts.utils import random_string_generator
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
		message = render_to_string('accounts/account_activation_email.html', {
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


class MyProfile(View):
	model = User
	template_name = 'accounts/my_profile.html'
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

