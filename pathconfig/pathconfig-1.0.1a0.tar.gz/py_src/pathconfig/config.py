##
# (c) 2006-2013 Yannick Versley / University of Tuebingen
# (c) 2015 Yannick Versley / University of Heidelberg
## Licensed under the Apache License, Version 2.0 (the "License"); you may
## not use this file except in compliance with the License.  You may obtain
## a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
## WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
## License for the specific language governing permissions and limitations
## under the License.

import sys
import os
import os.path
import yaml

#pylint:disable=R0903,C0103

class ConfigValue(object):
    '''
    a configurable value that can have templates variables in it that
    are subsequently filled from the environment.
    This means that the value retrieved from the YML config can have
    slots such as %(foo)s, which will then be filled by the env value
    for foo.
    '''
    def __init__(self, path, parent):
        self.path = path
        self.parent = parent

    def retrieve_value(self, env):
        "fetches the value for that entry"
        return self.parent.get_config_var(self.path, env)

    def __mod__(self, env):
        """fill in config value for string interpolation"""
        fmt = self.retrieve_value(env)
        return fmt % env


class AppContext(object):
    '''
    provides a context for one particular application
    '''
    def __init__(self, config_obj, data_dir):
        self.conf = config_obj
        self.data_dir = data_dir
    def get_config_var(self, path, env=None):
        '''
        retrieves the config variable named ``path`` from the config file.
        Path elements that start with a $ are replaced with values from the
        dict passed as ``env``
        '''
        if env is None:
            env = {}
        result = self.conf
        for e in path.split('.'):
            if e[0] == '$':
                try:
                    result = result[env[e[1:]]]
                except KeyError, ex:
                    try:
                        result = result['.default']
                    except KeyError:
                        raise ex
            else:
                result = result[e]
        return result
    def config_value(self, path):
        '''
        returns a ConfigValue object that can interact with
        '''
        return ConfigValue(path, self)
    def get_dirname(self, key):
        try:
            x = self.get_config_var('paths.%s_dir' % (key,))
        except KeyError:
            x = os.path.join(self.data_dir, key)
        if x[-1] == '/':
            return x
        else:
            return x + '/'


def load_configuration(app_name):
    '''
    creates a new configuration and loads the appropriate
    files.
    '''
    if sys.prefix == '/usr':
        conf_dir = '/etc'
        share_dir = '/usr/share'
    else:
        conf_dir = os.path.join(sys.prefix, 'etc')
        share_dir = os.path.join(sys.prefix, 'share')
    # Step 1: try to locate pynlp.yml
    yml_config = {}
    for fname in [
            '%s.yml'%(app_name,),
            os.path.expanduser('~/.%s.yml'%(app_name,)),
            os.path.join(conf_dir, '%s.yml'%(app_name,))]:
        if os.path.exists(fname):
            yml_config = yaml.load(file(fname))
            break
    try:
        data_dir = yml_config['paths']['data_dir']
    except KeyError:
        try:
            data_dir = os.environ[app_name.upper()]
        except KeyError:
            data_dir = os.path.join(share_dir, app_name)
    return AppContext(yml_config, data_dir)
