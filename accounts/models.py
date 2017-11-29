# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from posts.utils import random_string_generator
from rest_framework.authtoken.models import Token
# Create your models here.


class Profile(models.Model):
	user 			= models.OneToOneField(User)
	activation_key	= models.CharField(max_length=120, blank=True, null=True)
	activated		= models.BooleanField(default=False)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True) 

	def __str__(self):
		return '{} {}'.format(self.user, self.activated)

	def __unicode__(self):
		return '{} {}'.format(self.user, self.activated)


# class AuthorRequests(models.Model):
# 	STATUS_CHOICES = (
# 		('submitted','Submitted'),
# 		('aknowledged','Aknowledged'),
# 		('waiting_list','Waiting List'),
# 		('accepted', 'Accepted'),
# 		('rejected', 'Rejected'),
# 		)
# 	user 			= models.ForeignKey(User, related_name='author_requests')
# 	request_status 	= models.CharField(max_length=120, choices=STATUS_CHOICES, default = 'submitted')
# 	timestamp 		= models.DateTimeField(auto_now_add=True)
# 	updated 		= models.DateTimeField(auto_now=True) 
# 	description		= models.TextField()

# 	def __str__(self):
# 		return '{} {}'.format(self.user, self.request_status)

# 	def __unicode__(self):
# 		return '{} {}'.format(self.user, self.request_status)





@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		Token.objects.create(user=instance)
	instance.profile.save()
