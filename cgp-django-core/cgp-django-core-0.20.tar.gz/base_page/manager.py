from django.db import models


class PageQueryset(models.query.QuerySet):

    def published(self):
        """Return only Published Records"""
        return self.filter(state=20)

    def unpublished(self):
        """Return only Unpublished Records"""
        return self.filter(state__in = (10,15))


class PageManager(models.Manager):
    def get_query_set(self):
        """Gets Base Queryset"""
        return PageQueryset(self.model, using=self._db)

    def published(self):
        """Calls the Published Queryset"""
        return self.get_query_set().published()
    
    def unpublished(self):
        """Calls the Unpublished Queryset"""
        return self.get_query_set().unpublished()

