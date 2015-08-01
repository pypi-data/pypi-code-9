# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Paper
# Copyright 2015 ActivKonnect

from __future__ import unicode_literals

from django.db.models import signals
from django.core.cache import caches
from django.utils.six import wraps
from qualname import qualname

cache = caches['default']


def key_name(func):
    return '{module}.{name}'.format(
        module=func.__module__,
        name=qualname(func),
    )


def make_cache_key_tpl(name, version):
    return '{name}:pk{{pk}}_v{version}'.format(
        name=name,
        version=version,
    )


def listen_to_model(model, finder, key_tpl):
    to_handle = []

    def find_pks(instance):
        return [key_tpl.format(pk=pk)
                for pk in finder(instance).values_list('pk', flat=True)]

    # noinspection PyUnusedLocal
    def post_save_handler(instance, **kwargs):
        cache.delete_many(find_pks(instance))

    # noinspection PyUnusedLocal
    def pre_delete_handler(instance, **kwargs):
        to_handle.extend(find_pks(instance))

    # noinspection PyUnusedLocal
    def post_delete_handler(**kwargs):
        cache.delete_many(to_handle)
        del to_handle[:]

    signals.post_save.connect(post_save_handler, sender=model, weak=False)
    signals.pre_delete.connect(pre_delete_handler, sender=model, weak=False)
    signals.post_delete.connect(post_delete_handler, sender=model, weak=False)


def paper(version, dependencies):
    def decorator(func):
        key_tpl = make_cache_key_tpl(key_name(func), version)

        for model, finder in dependencies:
            listen_to_model(model, finder, key_tpl)

        @property
        @wraps(func)
        def wrapper(self):
            key = key_tpl.format(pk=self.pk)
            val = cache.get(key)

            if val is not None:
                return val

            val = func(self)
            cache.set(key, val, None)

            return val
        return wrapper
    return decorator
