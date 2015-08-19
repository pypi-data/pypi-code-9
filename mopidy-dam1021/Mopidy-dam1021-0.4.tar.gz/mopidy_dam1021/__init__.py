# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from mopidy import config, ext


__author__ = "Forta(a)"
__copyright__ = "Copyright 2015, Forta(a)"

__version__ = "0.4"
__maintainer__ = "Forta(a)"
__status__ = "Alpha"


class Extension(ext.Extension):
    dist_name = 'Mopidy-dam1021'
    ext_name = 'dam1021'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['serial'] = config.String()
        schema['volume_inf'] = config.Integer()
        schema['volume_sup'] = config.Integer()
        schema['timeout'] = config.Integer(optional=True)
        return schema

    def setup(self, registry):
        from mopidy_dam1021.mixer import Dam1021Mixer
        
        registry.add('mixer', Dam1021Mixer)
