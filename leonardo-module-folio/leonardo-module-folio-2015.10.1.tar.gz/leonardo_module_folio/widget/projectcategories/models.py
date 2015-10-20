# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _

from leonardo.models import ListWidget

from leonardo_module_folio.models import Category


class ProjectCategoriesWidget(ListWidget):

    def get_items(self):
        return Category.objects.filter(active=True)

    class Meta:
        abstract = True
        verbose_name = _("project categories")
        verbose_name_plural = _("project categories")
