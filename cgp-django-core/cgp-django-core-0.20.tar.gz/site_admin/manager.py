from django.db import models
from django.contrib import admin
from django.db.models import Q



class LegacyURLQueryset(models.query.QuerySet):

	def published(self):
		"""Return only Published Records"""
		return self.filter(state=20)

	def unpublished(self):
		"""Return only Unpublished Records"""
		return self.filter(state__in = (10,15))


class LegacyURLManager(models.Manager):
	def get_query_set(self):
		"""Gets Base Queryset"""
		return LegacyURLQueryset(self.model, using=self._db)

	def has_redirect(self):
		return self.exclude( Q(_redirect_path__isnull=True) | Q(_redirect_path='') )

	def needs_redirect(self):
		return self.filter( Q(_redirect_path__isnull=True) | Q(_redirect_path='') )