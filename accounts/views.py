# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import SignUpForm

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
		user = form.save()
		auth_login(self.request, user)
		return super(SignUpView, self).form_valid(form)

	def form_invalid(self, form):
		return super(SignUpView, self).form_invalid(form)