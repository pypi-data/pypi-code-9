# -*- coding: utf-8 -*-

"""Recipe ncwms"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, tomcat

config = Template(filename=os.path.join(os.path.dirname(__file__), "config.properties"))
wms_config = Template(filename=os.path.join(os.path.dirname(__file__), "config.xml"))

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs ncWMS2 with conda and setups WMS configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.prefix = self.options.get('prefix', conda.prefix())
        self.options['prefix'] = self.prefix
        self.options['config_dir'] = self.options.get(
            'config_dir', os.path.join(tomcat.content_root(self.prefix), 'ncWMS2'))
        self.options['data_root'] = self.options.get(
            'data_root', os.path.join(self.prefix, 'var', 'lib', 'pywps', 'outputs'))
        self.options['organization'] = self.options.get('organization', 'Birdhouse')
        self.options['url'] = self.options.get('url', 'http://bird-house.github.io/')

    def install(self):
        installed = []
        installed += list(self.install_conda())
        installed += list(self.install_config())
        installed += list(self.install_wms_config())
        return tuple()

    def install_conda(self):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'ncwms2'})

        return script.install()

    def install_config(self):
        result = config.render(**self.options)

        # make sure ncWMS2.war is unpacked
        tomcat.unzip(self.prefix, 'ncWMS2.war')

        output = os.path.join(tomcat.tomcat_home(self.prefix), 'webapps', 'ncWMS2', 'WEB-INF', 'classes', 'config.properties')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_wms_config(self):
        result = wms_config.render(**self.options)

        output = os.path.join(tomcat.content_root(self.prefix), 'ncWMS2', 'config.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def update(self):
        #self.install_conda()
        self.install_config()
        self.install_wms_config()
        return tuple()

def uninstall(name, options):
    pass

