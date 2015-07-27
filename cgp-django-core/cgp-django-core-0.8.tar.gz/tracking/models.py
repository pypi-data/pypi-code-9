from urlparse import urlparse
import urllib

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import Template, Context



class Event( models.Model ):

    domain = models.CharField(_("Domain"), blank=True, null=True, max_length=255,)
    path = models.CharField(_("Path"), blank=True, null=True, max_length=255,)
    full_url = models.CharField(_("Full URL"), blank=True, null=True, max_length=255,)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)

    category = models.CharField("Category", max_length=255, 
        null=True, blank=True)
    action = models.CharField("Action", max_length=255, 
        null=True, blank=True)
    label = models.CharField("Label", max_length=255, 
        null=True, blank=True)
    value = models.FloatField("Value", null=True, blank=True)
    
    content = models.TextField("Content", null=True, blank=True)
    user_agent = models.TextField("User Agent", null=True, blank=True)



    

    @classmethod
    def get_count(cls, category=None, action=None, label=None, from_datetime=None, \
        to_datetime=None, domain=None, path=None, full_url=None ):

        all_events = cls.objects.all()
        if category:
            all_events = all_events.filter(category=category)

        if action:
            all_events = all_events.filter(action=action)

        if label:
            all_events = all_events.filter(label=label)

        if from_datetime:
            all_events = all_events.filter(created__gte=from_datetime)

        if to_datetime:
            all_events = all_events.filter(created__lte=to_datetime)

        if domain:
            all_events = all_events.filter(domain=domain)

        if path:
            all_events = all_events.filter(path=path)

        if full_url:
            all_events = all_events.filter(full_url=full_url)

        return all_events

    @classmethod
    def track(cls, url, category=None, action=None, label=None, value=None, \
        content=None, ua=None):

        if url:
            parsed_uri = urlparse( url )
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            path = parsed_uri.path
        else:
            domain = None
            path = None

        track = cls(
            domain=domain,
            path=path,
            full_url=url,
            category=category,
            action=action,
            label=label,
            value=value,
            content=content,
            user_agent=ua
        )
        track.save()
        return track
