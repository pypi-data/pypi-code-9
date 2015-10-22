import sys
import os.path

# make sure this is run from inside the package
from . import config as mimodd_settings

class GalaxyAccess (object):
    CONFIG_FILE_GUESSES = ['config/galaxy.ini',
                           'universe_wsgi.ini']
    TOOL_CONFIG_FILE_REF = 'tool_config_file'
    pkg_galaxy_data_path = os.path.join(
        os.path.dirname(mimodd_settings.__file__),
        'galaxy_data')
    tool_conf_file = os.path.join(
        pkg_galaxy_data_path,
        'mimodd_tool_conf.xml')

    @classmethod
    def set_toolbox_path (cls):
        """Update the mimodd_tool_conf.xml file installed as part of the package
        with an absolute tool_path to the package xml wrappers."""
        
        with open(cls.tool_conf_file, 'r') as sample:
            template = sample.readlines()[1:]
        with open(cls.tool_conf_file, 'w') as out:
            out.write ('<toolbox tool_path="' + \
                       cls.pkg_galaxy_data_path + '">\n')
            out.writelines(template)

    def __init__ (self, galaxydir, config_file = None):
        if not os.path.isdir(galaxydir):
            raise OSError(
                '{0} does not seem to be a valid directory.'.format(galaxydir))
        self.galaxy_dir = galaxydir
        if config_file is None:
            self.config_file = self.get_config_file()
        else:
            self.config_file = config_file
        
    def get_config_file (self):
        for location_guess in self.CONFIG_FILE_GUESSES:
            config_file = os.path.join(self.galaxy_dir, location_guess)
            if os.path.isfile(config_file):
                return config_file
        raise OSError('Could not find Galaxy configuration file in default location.')

    def add_to_galaxy (self, line_token = None, force = False):
        """Register and install MiModD's tool wrappers for Galaxy."""
        
        if line_token is None:
            line_token = self.TOOL_CONFIG_FILE_REF
        self.set_toolbox_path()
        # update Galaxy's configuration file
        # to include mimodd_tool_conf.xml
        # as a tool_config_file
        with open(self.config_file, 'r') as config_in:
            config_data = config_in.readlines()
        for line_no, line in enumerate(config_data):
            if line.startswith(line_token + ' ='):
                try:
                    key, value = line.split('=')
                except ValueError:
                    raise OSError('Unexpected format of configuration file line {0}: {1}.'
                                  .format(line_no, line))
                conf_files = [file.strip() for file in value.split(',')]
                if self.tool_conf_file in conf_files:
                    print ('Galaxy is already configured correctly. No changes needed.')
                    print ('If Galaxy is currently running, you may still want to restart to make sure all changes are effective.')
                    return
                config_data[line_no] = line.rstrip() + ',' + \
                                       self.tool_conf_file + '\n'
                break
        else:
            raise OSError('Galaxy configuration file {0} has no {1} setting. Maybe the line "{2}" has been commented out ?'
                          .format(self.config_file, line_token, line_token + '= ...'))
        
        # ask for user backup before making changes to Galaxy config file
        print ('We recommend to back up the Galaxy configuration file {0} before proceeding !'
               .format(self.config_file))
        confirm = input ('Proceed (y/n)? ')
        if confirm != 'y' and confirm != 'Y':
            print ('No changes made to Galaxy configuration file. Aborting.')
            return

        # write changes to config file    
        with open(self.config_file, 'w') as config_out:
            try:
                config_out.writelines(config_data)
            except:
                raise OSError('We are very sorry, but an error has occurred while making changes to the Galaxy configuration file {0}. If you have made a backup of the file, you may want to use it now.'
                              .format(self.config_file))
                
        print ('Successfully updated the Galaxy configuration file {0} to include the MiModD tools.'
               .format(self.config_file))
        print ('If Galaxy is currently running, you will have to restart it for changes to take effect.')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(usage = argparse.SUPPRESS,
                                     formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description = """

integrate this installation of MiModD into a local Galaxy.

""")
    parser.add_argument('galaxydir', metavar = 'path_to_Galaxy', help = 'path to your local Galaxy installation')
    parser.add_argument('-c', '--config_file', default = argparse.SUPPRESS, help = 'provide the full path to the Galaxy configuration file directly')
    parser.add_argument('-t', '--token', dest = 'line_token', default = argparse.SUPPRESS, help = 'add the path to the MiModD Galaxy tool wrappers to this variable in the configuration file (default: tool_config_file)')
    args = vars(parser.parse_args())
    GalaxyAccess(args['galaxydir'],
                 args.get('config_file')).add_to_galaxy(args.get('line_token'))
    
