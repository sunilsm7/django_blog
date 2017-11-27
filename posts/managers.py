from django.db import models
from django.db.models import Q, F, Count


class PostQuerySet(models.QuerySet):
	def drafts(self):
		return self.filter(draft = True)

	def published(self):
		return self.filter(
			Q(draft = False),
			Q(approved = True)
			)

	def approved(self):
		return self.filter(approved = True)

	def search(self, query):
		if query:
			query = query.strip()
			return self.filter(
				Q(draft=False),
				Q(approved = True),
				Q(title__icontains = query) |
				Q(content__icontains = query) |
				Q(user__username__istartswith = query)
				)
		return self


class PostManager(models.Manager):
	def get_queryset(self):
		return PostQuerySet(self.model, using = self._db)

	def drafts(self):
		return self.get_queryset().drafts()

	def published(self):
		return	self.get_queryset().published()

	def search(self, query):
		return self.get_queryset().search(query)

	def approved(self):
		return self.get_queryset().approved()
