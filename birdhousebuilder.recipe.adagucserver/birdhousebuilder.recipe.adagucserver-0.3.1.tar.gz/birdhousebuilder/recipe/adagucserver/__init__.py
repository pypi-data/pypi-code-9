# -*- coding: utf-8 -*-

"""Recipe adagucserver"""

import os
import subprocess
from mako.template import Template

from birdhousebuilder.recipe import conda, supervisor, nginx

templ_app = Template(filename=os.path.join(os.path.dirname(__file__), "adagucserver.py"))
templ_autowms = Template(filename=os.path.join(os.path.dirname(__file__), "autowms.xml"))
templ_gunicorn = Template(filename=os.path.join(os.path.dirname(__file__), "gunicorn.conf.py"))
templ_cmd = Template(
    "${prefix}/bin/gunicorn adagucserver:app -c ${prefix}/etc/gunicorn/adagucserver.py")

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        
        self.prefix = self.options.get('prefix', conda.prefix())
        self.options['prefix'] = self.prefix

        self.hostname = options.get('hostname', 'localhost')
        self.options['hostname'] = self.hostname
        self.port = options.get('port', '9002')
        self.options['port'] = self.port

        self.options['title'] = self.options.get('title', 'Birdhouse ADAGUC WMS')
        self.options['abstract'] = self.options.get('abstract', 'ADAGUC Web Map Service used in Birdhouse')
        self.options['online_resource'] = 'http://%s:%s/?' % (self.hostname, self.port)
        self.options['font'] = os.path.join(self.prefix, 'share','adagucserver','fonts', 'FreeSans.ttf')
        self.options['db_params'] = os.path.join(self.prefix, 'var', 'lib', 'adagucserver', 'adagucserver.db')
        self.options['data_dir'] = os.path.join(self.prefix, 'var', 'lib', 'pywps', 'outputs')
        self.options['enablecache'] = self.options.get('enablecache', 'false')
              
    def install(self, update=False):
        installed = []
        installed += list(self.install_pkgs(update))
        installed += list(self.install_app())
        installed += list(self.install_config())
        installed += list(self.install_db())
        installed += list(self.install_gunicorn())
        installed += list(self.install_supervisor(update))
        installed += list(self.install_nginx(update))
        return tuple()

    def install_pkgs(self, update=False):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'adagucserver gunicorn'})
        if update == True:
            script.update()
        else:
            script.install()
        return tuple()

    def install_app(self):
        result = templ_app.render(
            prefix=self.prefix,
            )
        output = os.path.join(self.prefix, 'etc', 'adagucserver', 'adagucserver.py')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]
        
    def install_config(self):
        """
        install adagucserver config in etc/adagucserver
        """

        # setup configured dirs
        conda.makedirs(os.path.join(self.prefix, 'var', 'cache', 'adagucserver'))

        # generate config
        result = templ_autowms.render(**self.options)
        output = os.path.join(self.prefix, 'etc', 'adagucserver', 'autowms.xml')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_db(self):
        conda.makedirs(os.path.join(self.prefix, 'var', 'lib', 'adagucserver'))
        try:
            subprocess.check_call([
                os.path.join(self.prefix, 'bin', 'adagucserver'),
                '--updatedb',
                '--config',
                os.path.join(self.prefix, 'etc', 'adagucserver', 'autowms.xml')])
        except:
            print "Failed to run adagucserver updatedb"
        return tuple()
    
    def install_gunicorn(self):
        """
        install etc/gunicorn/adagucserver.py
        """
        result = templ_gunicorn.render(
            prefix=self.prefix,
            )
        output = os.path.join(self.prefix, 'etc', 'gunicorn', 'adagucserver.py')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_supervisor(self, update=False):
        script = supervisor.Recipe(
            self.buildout,
            'adagucserver',
            {'program': 'adagucserver',
             'command': templ_cmd.render(prefix=self.prefix),
             'directory': os.path.join(self.prefix, 'etc', 'adagucserver')
             })
        if update == True:
            script.update()
        else:
            script.install()
        return tuple()

    def install_nginx(self, update=False):
        script = nginx.Recipe(
            self.buildout,
            self.name,
            {'input': os.path.join(os.path.dirname(__file__), "nginx.conf"),
             'sites': 'adagucserver',
             'prefix': self.prefix,
             'port': self.port,
             'hosename': self.hostname,
             })
        if update == True:
            script.update()
        else:
            script.install()
        return tuple()
        
    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

