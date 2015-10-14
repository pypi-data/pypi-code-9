"""
Models for generic rating.

"""
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import DecimalField
from django.contrib.contenttypes import generic

from changer.c5.rating.managers import RatedItemManager, RateManager

class RatedItem(models.Model):
    """
    Rate info for an object.
    
    """
    rate_average = models.FloatField(_('rating average'))
    rate_count = models.PositiveIntegerField(_('rating count'))
    
    last_rated_on = models.DateTimeField(_('last rate on'), editable=False,
                                         null=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length="80")
    object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = RatedItemManager()
    
    @property
    def rounded_average(self):
        return int(round(self.rate_average))
    
    class Meta:
        verbose_name = _('rated item')
        verbose_name_plural = _('rated items')
        unique_together = (('content_type', 'object_id'),)
    
    def __str__(self):
        return _('Rating for %s') % self.object
        
    def add_rate(self, value, user):
        now = datetime.datetime.now()
        value = int(value)
        
        #Add rate object and allow only 1 vote per user
        rate, created = self.rates.get_or_create(rated_object=self, user=user)
        rate.rate = value
        rate.date = now
        rate.save()
        
        #Alter rated item object to reflect changes
        if created:
            self.rate_count += 1        
        self.rate_average = Rate.objects.rate_average(self.object)
        self.last_rated_on = now
        self.save()
        
        #Denormalized data in linked model is added
        obj = self.object
        denormalized = False
        if hasattr(obj, 'rating'):
            obj.rating = self.rate_average
            denormalized = True
        if hasattr(obj, 'rating_total'):
            obj.rating_total = self.rate_count
            denormalized = True
        if denormalized:
            obj.save()
        return self
    
    def get_average(self):
        return '%.1f' % self.rate_average
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.rate_count = 0
            self.rate_average = 0
        super(RatedItem, self).save(*args, **kwargs)

class Rate(models.Model):
    """
    Rate detail.

    """
    rated_object = models.ForeignKey('RatedItem', related_name='rates')
    user = models.ForeignKey(User, verbose_name=_('user'), null=True,
                             blank=True)
    rate = models.PositiveSmallIntegerField(_('rating value'), null=True)
    date = models.DateTimeField(_('rated on'), editable=False)

    objects = RateManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = datetime.datetime.now()
        super(Rate, self).save(*args, **kwargs)
