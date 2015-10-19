# -*- coding: utf-8 -*-
"""The tgapp-samlauth package"""
from saml2.client import Saml2Client
from tg import hooks
from tg.configuration.utils import coerce_config
from tg.support.converters import aslist

import logging
log = logging.getLogger('tgapp-samlauth')


def plugme(app_config, options):
    if options is None:
        options = {}

    config_namespace = options.get('config_namespace', 'samlauth')
    if not config_namespace.endswith('.'):
        config_namespace += '.'

    userdata_adapter = options.get('userdata_adapter')
    if userdata_adapter is None:
        raise ValueError('A userdata_adapter callable option is required to gather userid for TG to log the user in.')

    log.info('Configuring tgapp-samlauth from "{}.*" options'.format(config_namespace))
    authconf = SAMLAuthConfiguration({
        'config_namespace': config_namespace,
        'userdata_adapter': userdata_adapter
    })
    hooks.register('configure_new_app', authconf.on_app_configured)

    return dict(appid='samlauth',
                plug_helpers=False,
                plug_models=False,
                plug_bootstrap=False,
                plug_statics=False)


class SAMLAuthConfiguration(object):
    def __init__(self, options):
        self.options = options

    def on_app_configured(self, app):
        conf = coerce_config(app.config, self.options['config_namespace'], {
            'config_file': str,
            'enc_key_files': aslist
        })

        sp = Saml2Client(config_file=conf['config_file'])
        sp.config_file = conf['config_file']
        sp.user_data_adapter = self.options['userdata_adapter']
        if conf.get('enc_key_files'):
            # Looks like PySAML has no way to configure enc_key_files
            # from config file, so we configure them from here.
            sp.sec.enc_key_files = conf['enc_key_files']

        app.config['tg.app_globals'].samlsp = sp