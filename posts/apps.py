# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'

    def ready(self):
        import posts.signals
