# -*- coding: utf-8 -*-
"""The tgapp-contactform package"""
from tg import hooks
from tg.configuration.utils import coerce_config
from tg.support.converters import aslist


def plugme(app_config, options):
    if options is None:
        options = {}

    config_namespace = options.get('config_namespace', 'contactform')
    if not config_namespace.endswith('.'):
        config_namespace += '.'

    configurator = ContactFormConfigurator(
        config_namespace=config_namespace
    )
    hooks.register('configure_new_app', configurator.on_app_configured)

    return dict(appid='contactform',
                plug_helpers=False,
                plug_models=False,
                plug_bootstrap=False,
                plug_statics=False)


class ContactFormConfigurator(object):
    def __init__(self, config_namespace):
        self.config_namespace = config_namespace

    def on_app_configured(self, app):
        conf = coerce_config(app.config, self.config_namespace, {
            'sender': str,
            'recipients': aslist
        })

        if not conf.get('sender'):
            raise ValueError('contactform requires "{}sender" option'.format(self.config_namespace))

        if not conf.get('recipients'):
            raise ValueError('contactform requires "{}recipients" option'.format(self.config_namespace))

        app.config['_contactform'] = conf

