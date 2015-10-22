from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class BlogConfig(AppConfig):
    """
    Config for Zinnia application.
    """
    name = 'luhublog'
    label = 'luhublog'
    verbose_name = _('Blog')