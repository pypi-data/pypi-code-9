# -#- coding: utf-8 -#-

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import ListWidget
from newswall.models import Source, Story


class RecentNewsWidget(ListWidget):
    post_count = models.PositiveIntegerField(
        verbose_name=_("post count"), default=3)
    show_button = models.BooleanField(
        default=True, verbose_name=_("show link button"))

    sources = models.ManyToManyField(
        Source, blank=True, verbose_name=_("Sources"))

    def render_content(self, options):
        request = options.get('request')
        context = {'widget': self, 'request': request}

        stories = Story.objects.filter(source__id__in=self.sources.all())[:self.post_count]

        self.set_items(stories)

        context['entries'] = stories

        return render_to_string(self.get_template, context)

    class Meta:
        abstract = True
        verbose_name = _("recent news")
        verbose_name_plural = _("recent news")
