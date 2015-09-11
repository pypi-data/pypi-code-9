# -*- coding: utf-8 -*-
"""
This module contains the generation of apache configuration
"""

import re
import os
import zc.buildout
from Cheetah.Template import Template

#plone.org:127.0.0.1:3128
BACKEND_PATTERN =  re.compile("([^:]*):([^:]*):([0-9]+)")
VHM_PATTERN = re.compile("([^:]*):/(.*)")
VHM_PATH = re.compile("([^/]*)/(.*)")
BIND_PATTERN = re.compile("([^:]*):([0-9]+)$")
NUMBER_PATTERN = re.compile("^([0-9]+)$")
RECIPE_BUILD_NAME = 'plone.recipe.apache:build'
RESOURCE_PATTERN = re.compile("([^:]*):(.*)")
RESOURCE_EXPIRES = re.compile("([^:]*):(.*)")
RESOURCE_HEADERS = re.compile("([^:]*):([^:]*):(.*)")
REDIRECT_PATTERN = re.compile("([^:]*):(.*)")

current_dir = os.path.dirname(__file__)

def _get_location(buildout):
    """ get the name of config file """
    for part in buildout.keys():

        if buildout[part].has_key('recipe') and \
            buildout[part]['recipe'] == RECIPE_BUILD_NAME:

            return os.path.join(buildout[part]['location'],'conf','httpd.conf')
    return None


class ConfigureRecipe(object):
    """This recipe is used by zc.buildout
    for configuring apache
    """

    def __init__(self, buildout, name, options):
        self.name, self.options = name, options

        location = options.get(
            'location', buildout['buildout']['parts-directory'])
        self.options['location'] = location
        self.options['prefix'] = os.path.join(location, name)
        self.options['binary_location'] =  os.path.join(\
                                        buildout['buildout']['directory'],
                                        'bin')

        self.options['mainconfig'] = self.options.get('mainconfig',
                                                      _get_location(buildout)
                                                      )
        self.options['bind'] = str(self.options.get('bind', '*:80'))

        m = BIND_PATTERN.match(self.options['bind'])
        if m:
            self.options['port'] = m.groups()[1]
        elif NUMBER_PATTERN.match(self.options['bind'] ):
            self.options['port'] = self.options['bind']
            self.options['bind'] = "*:%s" % (self.options['port'])


        # var directory for cache storage and pid file
        base_dir = buildout['buildout']['directory']
        var_dir = self.options.get('var', os.path.join(base_dir, 'var'))

        # log directory
        log_dir = os.path.join(var_dir, 'log')
        self.options['var_dir'] = var_dir
        self.options['log_dir'] = log_dir
        self.options['log_format'] = self.options.get('log_format','common')
        self.options['etag'] = self.options.get('etag','')
        self.options['compression'] = self.options.get('compression','')
        self.options['extras'] = self.options.get('extras','')

        # compute backend
        backends = self.options.get('backends','').splitlines()
        self.backends = []
        for b in backends:
            m = BACKEND_PATTERN.match(b)
            if m:
                (host,backend_host,backend_port) = m.groups()
                vhm = VHM_PATH.match(host)
                if vhm:

                    (host, _vhm_path) =  vhm.groups()
                else:
                    _vhm_path = None

                self.backends.append({'host': host.strip(),
                                      '_vhm_path': _vhm_path and _vhm_path.strip(),
                                      'backend_host' : backend_host,
                                      'backend_port' : backend_port})


        # compute vhm
        vhm_map = self.options.get('zope2_vhm_map','').splitlines()
        self.zope2_vhm_maps = {}
        for vhm in vhm_map:
            # vhm is like plone2.org/plone
            m = VHM_PATTERN.match(vhm)
            if m:
                (host,vhm_path) = m.groups()
                host = host.strip()
                if not self.zope2_vhm_maps.has_key(host):
                    self.zope2_vhm_maps[host] = []
                self.zope2_vhm_maps[host].append(vhm_path.strip())

        # compute resources
        resources = self.options.get('resources','').splitlines()
        self.resources_map = []
        for resource in resources:
            m = RESOURCE_PATTERN.match(resource)
            if m:
                url, path = m.groups()
                self.resources_map.append({'url': url.strip(), 'path': path.strip()})

        # compute resource expires
        resources = self.options.get('resource-expires','').splitlines()
        self.filematch_map = {}
        for resource in resources:
            m = RESOURCE_EXPIRES.match(resource)
            if m:
                match, value = m.groups()
                fm = self.filematch_map.setdefault(match.strip(), {})
                fm['expires'] = value.strip()
                fm['headers'] = []

        # compute resource headers
        resources = self.options.get('resource-headers','').splitlines()
        for resource in resources:
            m = RESOURCE_HEADERS.match(resource)
            if m:
                match, header, value = m.groups()
                fm = self.filematch_map.setdefault(match.strip(), {})

                # make sure expires is set
                fm.setdefault('expires', '')

                # append headers in order
                headers = fm.setdefault('headers', [])
                headers.append({'header':header.strip(), 'value':value.strip()})

        # compute redirects
        redirects = self.options.get('redirects','').splitlines()
        self.redirects_map = {}
        for redirect in redirects:
            m = REDIRECT_PATTERN.match(redirect)
            if m:
                servername, target = m.groups()
                target = target.strip()
                if not self.redirects_map.has_key(target):
                    self.redirects_map[target] = []
                self.redirects_map[target].append({'servername': servername.strip()})

        # put all config in this directory
        self.options['config_dir'] =  os.path.join(self.options['prefix'],'conf.d')


    def install(self):
        """installer"""
        self._create_all_directory()
        self._verify_config(self.options['mainconfig'])
        self._make_apacheconf()
        return self.options['config_dir']


    def _create_all_directory(self):
        for dir in ('config_dir','var_dir', 'log_dir'):
            try:
                os.makedirs(self.options[dir])
            except OSError,e:
                # file exists
                if e.errno == 17:
                    pass
            except WindowsError,e:
                # file exists
                pass
            except Exception,e:
                # other raise
                raise e




    def _verify_config(self, config_file):
        """ test if the config is good or not """
        if not os.access(config_file, os.R_OK):
            raise  IOError,"Can not read mainconfig %s" % (config_file,)

    def _make_apacheconf(self):
        """ make apache conf """
        file_name = os.path.join(current_dir,'templates', 'inner_vhost.conf.tmpl')
        tpl = Template(file=file_name)

        for backend in self.backends:

            tpl.backend = backend
            tpl.host = backend['host']
            tpl.zope2_vhm_maps = self.zope2_vhm_maps.get(backend['host'], None)
            tpl.bind = self.options['bind']
            tpl.log_dir = self.options['log_dir']
            tpl.port = self.options['port']
            tpl.log_format = self.options['log_format']
            tpl.etag = self.options['etag']
            tpl.compression = self.options['compression']
            tpl.extras = self.options['extras']
            tpl.resources_map = self.resources_map
            tpl.redirects_map = self.redirects_map.get(backend['host'], None)
            tpl.filematch_map = fm = []
            for match, value in sorted(self.filematch_map.items()):
                value = value.copy()
                value['match'] = match
                fm.append(value)
            fd = open(os.path.join(self.options['config_dir'],
                                   "virtual_%s.conf" % (backend['host'],) ),'w')

            print  >> fd, tpl

        fd = open(self.options['mainconfig'])
        content = fd.read()
        fd.close()
        include = "Include %s/*.conf\n" % self.options['config_dir']
        if include not in content:
            if os.access(self.options['mainconfig'], os.W_OK):
                fd = open(self.options['mainconfig'],'a')
                fd.write("Include %s/*.conf\n" % self.options['config_dir'])

                fd.close()
            else:
                print "\nThe file %s is not  writable" % self.options['mainconfig']
                print "Please ask your system adminsitrator to add the following line in it:\n"
                print "Include %s/*.conf\n\n" % self.options['config_dir']
