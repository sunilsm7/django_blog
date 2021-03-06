# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.html import mark_safe
from markdown import markdown

from posts.search import PostIndex
from .managers import PostManager
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120)
    image = models.ImageField(
        upload_to='media/',
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    read_time = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()
    # objects  = models.Manager()

    class Meta:
        verbose_name_plural = "01 Posts"
        ordering = ['-timestamp', ]

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    # Add indexing method to Post
    def indexing(self):
        obj = PostIndex(
            meta={'id': self.id},
            user=self.user.username,
            title=self.title,
            slug=self.slug,
            content=self.content,
            draft=self.draft,
            height_field=self.height_field,
            width_field=self.width_field,
            approved=self.approved,
            publish=self.publish,
            views=self.views,
            updated=self.updated,
            timestamp=self.timestamp
        )

        obj.save()
        return obj.to_dict(include_meta=True)

    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def get_absolute_url(self):
        return reverse_lazy('posts:details', args=[str(self.id)])

    def get_post_views(self):
        return self.views

    @property
    def get_comments(self):
        # qs = Comment.objects.filter(post=self)
        qs = self.comments.all()
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '02 Comments'
        ordering = ['-timestamp']

    # def get_parent_comment(self):
    #   return Comment.objects.filter(parent=self.parent)

    def __str__(self):
        return '{} {}'.format(self.user, self.content, self.parent)

    def __unicode__(self):
        return '{} {}'.format(self.user, self.content, self.parent)

    # def get_absolute_url(self):
    #   return reverse_lazy('posts:replies', args=[str(self.post.id), str(self.id)])

    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def has_replies(self):
        return Comment.objects.filter(parent=self)
