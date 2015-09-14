from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.cache import cache

import string
import random


class HealthView(View):

    def get(self, request, *args, **kwargs):

        return HttpResponse(status=200)


class CacheHealthView(View):

    def get(self, request, *args, **kwargs):

        # Create a random cache key to avoid collision
        cache_key = ''.join(random.choice(string.ascii_letters) for _ in range(100))

        # Set the key in the cache and see if we can pull it out.
        cache.set(cache_key, 'works')

        # If so, return 200
        if cache.get(cache_key) == 'works':
            return HttpResponse(status=200)

        # If not, return 404
        return HttpResponseNotFound()
