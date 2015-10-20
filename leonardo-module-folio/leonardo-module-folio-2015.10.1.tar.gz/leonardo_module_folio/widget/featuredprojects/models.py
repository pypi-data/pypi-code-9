# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.models import ListWidget
from leonardo_module_folio.models import Project


class FeaturedProjectsWidget(ListWidget):
    project_count = models.PositiveIntegerField(
        verbose_name=_("project count"), default=2)
    show_link = models.BooleanField(default=True, verbose_name=_("show link button"))

    def get_projects(self):
        return Project.objects.filter(active=True, featured=True)[:self.project_count]

    def get_items(self):
        return self.get_projects()

    class Meta:
        abstract = True
        verbose_name = _("featured projects")
        verbose_name_plural = _("featured projects")
