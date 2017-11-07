# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
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
		current_site = get_current_site(request)
		subject = 'Activate Your MySite Account'
		message = render_to_string('accounts/account_activatin_email.html', {
			'user' : user,
			'domain' : current_site.domain,
			'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
			'activation_key' : account_activation_token.make_token(user),
			})
		user.email_user(subject, message)
		return redirect('home')
		# auth_login(self.request, user)
		# return super(SignUpView, self).form_valid(form)

	def form_invalid(self, form):
		return super(SignUpView, self).form_invalid(form)


class MyProfile(View):
	model = User
	template_name = 'accounts/my_profile.html'
	context_object_name = 'user_posts'
	paginate_by = 10
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'user_posts': self.context_object_name})

