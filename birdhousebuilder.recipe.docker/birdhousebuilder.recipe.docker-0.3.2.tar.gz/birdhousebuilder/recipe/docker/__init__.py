# -*- coding: utf-8 -*-

"""Recipe docker"""

import os
from mako.template import Template

templ_dockerfile = Template(filename=os.path.join(os.path.dirname(__file__), "Dockerfile"))

class Recipe(object):
    """Buildout recipe to generate a Dockerfile."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name = buildout, name
        b_options = buildout['buildout']
        self.buildout_dir = b_options.get('directory')

        self.options = dict()
        self.options['image_name'] = options.get('image-name', 'birdhouse/bird-base')
        self.options['image_version'] = options.get('image-version', 'latest')
        self.options['maintainer'] = options.get('maintainer', 'https://github.com/bird-house')
        self.options['description'] = options.get('description', 'Web Processing Service')
        self.options['vendor'] = options.get('vendor', 'Birdhouse')
        self.options['version'] = options.get('version', '1.0.0')
        self.options['http_port'] = options.get('http-port', '8094')
        self.options['https_port'] = options.get('https-port', '28094')
        self.options['output_port'] = options.get('output-port', '8090')

    def install(self):
        installed = []
        installed += list(self.install_dockerfile())
        return installed

    def install_dockerfile(self):
        result = templ_dockerfile.render(**self.options)
        output = os.path.join(self.buildout_dir, 'Dockerfile')
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
            os.chmod(output, 0o644)
        return [output]

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

