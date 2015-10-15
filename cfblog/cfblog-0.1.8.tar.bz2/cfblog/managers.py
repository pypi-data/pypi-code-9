import datetime

from django.db import models


class ContentManager(models.Manager):

    def published(self):
        return self.get_queryset().filter(status__gte=2, publish__lte=datetime.datetime.now())

    def static_pages(self):
        return self.get_queryset().filter(category__id=1)
