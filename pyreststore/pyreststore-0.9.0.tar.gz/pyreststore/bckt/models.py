# -*- coding: utf-8; mode: Python; -*-
from __future__ import unicode_literals

import logging
from django.conf import settings
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Bckt(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # Requested Time To Live is 1 week = 60*60*24*7 = 604800 seconds
    reqttl = models.IntegerField(blank=True, default=604800)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='python',
                                max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly',
                             max_length=100)
    owner = models.ForeignKey('auth.User', related_name='bckts')
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the bucket.
        """
        logger = logging.getLogger(__name__)
        logger.debug('Enter function')
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Bckt, self).save(*args, **kwargs)

        # Optionally limit the number of instances retained
        if settings.PYRESTSTORE_MAX_BCKTS and \
           settings.PYRESTSTORE_MAX_BCKTS > 0:
            bckts = Bckt.objects.all()
            overshoot = len(bckts) - settings.PYRESTSTORE_MAX_BCKTS
            #
            if overshoot > 0:
                s = '{}{}{:d}.'.format(
                    'The maximum number of Bckts ',
                    'to retain has been exceeded. Deleting ',
                    overshoot
                )
                logger.info(s)
                s = '{}{:d}'.format('PYRESTSTORE_MAX_BCKTS=',
                                    settings.PYRESTSTORE_MAX_BCKTS)
                logger.debug(s)
                logger.debug('Before: len(bckts)={:d})'.format(len(bckts)))
                for n in xrange(0, overshoot):
                    bckts[n].delete()
                bckts = Bckt.objects.all()
                logger.debug('After: len(bckts)={:d})'.format(len(bckts)))
        logger.debug('Returning from function')
