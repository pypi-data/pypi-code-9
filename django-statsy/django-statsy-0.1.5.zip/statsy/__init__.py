# coding: utf-8

from django.utils.module_loading import autodiscover_modules

from statsy.log import logger
from statsy.sites import site


__all__ = [
    'send', 'watch', 'get_send_params'
    'objects', 'groups', 'events',
    'site', 'autodiscover', 'logger'
]


def autodiscover():
    autodiscover_modules('stats', register_to=site)


def init_signals():
    import statsy.signals


def init_globals():
    from statsy.core import Statsy

    globals().update({
        'objects': Statsy.objects,
        'groups': Statsy.groups,
        'events': Statsy.events,

        '_statsy': Statsy()
    })

    globals().update({
        'send': _statsy.send,
        'watch': _statsy.watch,
        'get_send_params': _statsy.get_send_params
    })


default_app_config = 'statsy.apps.StatsyConfig'

