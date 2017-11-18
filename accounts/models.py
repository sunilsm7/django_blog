# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from posts.utils import random_string_generator
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


# def save_profile(sender, instance, **kwargs):
# 	instance.profile.save()

# post_save.connect(save_profile, sender=User)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()
