from datetime import *
from decimal import *
from django.contrib.sitemaps import Sitemap

from .models import *

class PageSitemap(Sitemap):
    
    def items(self):
        return Page.objects.filter(state__gte=PageBase.PUBLISHED)
        
    def lastmod(self, obj):
        return obj.modified

    def priority(self, obj):
        return obj.sitemap_priority

    def location(self, obj):
        return obj.get_absolute_url()

    def changefreq(self, obj):
        return obj.sitemap_changefreq
