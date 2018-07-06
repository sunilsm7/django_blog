from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .utils import unique_slug_generator
from .models import Post


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Post)


def index_post(sender, instance, *args, **kwargs):
    instance.indexing()


post_save.connect(index_post, sender=Post)
