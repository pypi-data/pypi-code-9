import re
from unidecode import unidecode
from django.db.models.signals import m2m_changed
from haystack import indexes

from .models import *


class BaseUserIndex(indexes.SearchIndex, indexes.Indexable):

    # -- Compiled Text to Index
    text = indexes.CharField(document=True, use_template=True)

    # -- Facets and Autocompletes
    full_name_auto = indexes.EdgeNgramField()
    email_auto = indexes.EdgeNgramField(model_attr='email')

    # -- Model Fields
    first_name = indexes.CharField(model_attr='first_name', indexed=True,
        stored=True)
    last_name = indexes.CharField(model_attr='last_name', indexed=True,
        stored=True)
    email = indexes.CharField(model_attr='email', indexed=True,
        stored=True)
    slug = indexes.CharField(model_attr='slug', indexed=True,
        stored=True, null=True)
    title = indexes.CharField(model_attr='title', indexed=True,
        stored=True)
    
   
    facebook_url = indexes.CharField(model_attr='facebook_url', indexed=True,
        stored=True, null=True)
    twitter_url = indexes.CharField(model_attr='twitter_url', indexed=True,
        stored=True, null=True)
    googleplus_url = indexes.CharField(model_attr='googleplus_url', indexed=True,
        stored=True, null=True)
    linkedin_url = indexes.CharField(model_attr='linkedin_url', indexed=True,
        stored=True, null=True)
    social_email = indexes.CharField(model_attr='social_email', indexed=True,
        stored=True, null=True)
    website = indexes.CharField(model_attr='website', indexed=True,
        stored=True, null=True)


    # -- Derived Values
    get_full_name = indexes.CharField(indexed=False, stored=True)
    full_name = indexes.CharField()
    last_name_sort = indexes.CharField(indexed=False, stored=True)
    first_name_sort = indexes.CharField(indexed=False, stored=True)
    
    is_searchable = indexes.BooleanField(indexed=False)

    # -- Template Fragments
    

    #TODO --override in subclass
    def get_model(self):
        return None

    def index_queryset(self, using = None):
        return self.get_model().objects.active()

    def prepare_full_name_auto(sefl, obj):
        return obj.get_full_name()
        
    def prepare_full_name(self, obj):
        return obj.get_full_name()

    def prepare_last_name_sort(self, obj):
        name = ''
        if obj.last_name:
            name += obj.last_name
        if obj.first_name:
            name += obj.first_name
        return format_text_for_sort( name)

    def prepare_first_name_sort(self, obj):
        name = ''
        if obj.first_name:
            name += obj.first_name

        if obj.last_name:
            name += obj.last_name
        
        return format_text_for_sort( name)

    def prepare_is_searchable(self, obj):
        return False


def format_text_for_sort(sort_term,remove_articles=False):
    ''' processes text for sorting field:
        * converts non-ASCII characters to ASCII equivalents
        * converts to lowercase
        * (optional) remove leading a/the
        * removes outside spaces
    '''
    sort_term = unidecode(sort_term).lower().strip()
    if remove_articles:
        sort_term =  re.sub(r'^(a\s+|the\s+)', '', sort_term )
    return sort_term
