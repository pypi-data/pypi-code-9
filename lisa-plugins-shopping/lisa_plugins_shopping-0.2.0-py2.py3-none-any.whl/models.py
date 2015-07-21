from django.db import models
from jsonfield import JSONField
from lisa_api.lisa.logger import logger


class ShoppingList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    list = JSONField(default={"items": []})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.lower()
        # check if list contains the required fields
        try:
            if 'items' in self.list:
                super(ShoppingList, self).save(force_insert, force_update)
            else:
                logger.error('The list does not contains an item field')
        except ValueError:
            logger.error('The list does not contains an item field')
