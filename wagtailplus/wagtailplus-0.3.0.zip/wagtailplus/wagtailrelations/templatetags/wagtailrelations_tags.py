"""
Contains application template tags.
"""
from django import template

from ..models import Entry


register = template.Library()

@register.assignment_tag()
def get_related(page):
    """
    Returns list of related Entry instances for specified page.

    :param page: the page instance.
    :rtype: list.
    """
    related = []
    entry   = Entry.get_for_model(page)

    if entry:
        related = entry.related

    return related

def get_related_with_scores(page):
    """
    Returns list of related tuples (Entry instance, score) for
    specified page.

    :param page: the page instance.
    :rtype: list.
    """
    related = []
    entry   = Entry.get_for_model(page)

    if entry:
        related = entry.related_with_scores

    return related
