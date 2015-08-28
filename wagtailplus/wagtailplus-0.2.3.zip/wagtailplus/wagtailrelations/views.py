"""
Contains application views.
"""
from django.views.generic import (
    ListView,
    TemplateView
)

from .models import (
    Category,
    Entry
)

class CategoriesView(ListView):
    """
    Renders site map index view (with pagination).
    """
    model           = Category
    queryset        = Category.live_entries.all()
    template_name   = 'wagtailrelations/site_map/index.html'

class EntriesView(TemplateView):
    """
    Renders site map entries for selected category.
    """
    template_name = 'wagtailrelations/site_map/entries.html'

    def get_context_data(self, **kwargs):
        """
        Returns view context dictionary.

        :rtype: dict.
        """
        kwargs.update({
            'entries': Entry.objects.get_for_tag(
                self.kwargs.get('slug', 0)
            )
        })

        return super(EntriesView, self).get_context_data(**kwargs)
