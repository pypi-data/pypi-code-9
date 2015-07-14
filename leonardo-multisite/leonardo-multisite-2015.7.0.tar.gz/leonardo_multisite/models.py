
from allowedsites import CachedAllowedSites
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
post_save.connect(CachedAllowedSites.update_cache, sender=Site,
                  dispatch_uid='update_allowedsites')
