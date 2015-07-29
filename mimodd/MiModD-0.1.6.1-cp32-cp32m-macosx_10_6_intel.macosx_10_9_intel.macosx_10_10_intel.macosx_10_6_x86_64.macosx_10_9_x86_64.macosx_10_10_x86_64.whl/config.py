import os, sys
from . import cfg
from . import ConfigParseError

class Config (object):
    __file__ = __file__
    _cfg_path = cfg.__file__
    _configurable_params = (
        'tmpfiles_path',
        'max_memory',
        'snpeff_path',
        'multithreading_level')
    _path_params = (
        'tmpfiles_path',
        'snpeff_path')
        
    tmpfiles_path = cfg.tmpfiles_path
    max_memory = cfg.max_memory
    multithreading_level = cfg.multithreading_level
    snpeff_path = cfg.snpeff_path

    bin_path = os.path.normpath(os.path.join(cfg.__file__, cfg.bin_path))
    samtools_exe = os.path.join(bin_path, 'samtools')
    bcftools_exe = os.path.join(bin_path, 'bcftools')
    samtools_legacy_exe = os.path.join(bin_path, 'samtools_legacy')
    snap_exe = os.path.join(bin_path, 'snap')

    def __init__ (self):
        """Configure a new Config instance based on environment variables."""
        
        new_config = os.getenv('MIMODD_CONFIG_UPDATE')
        if new_config:
            settings = {
                param: value for param, value in self.parse_env_config(
                    new_config)
                }
            if self.update_settings(settings):
                self.write_config()
                
        # see if we are running inside Galaxy
        # if so respect the framework's multithreading settings
        # otherwise use cfg file setting
        
        galaxy_slots = self.adjust_galaxy_slots(
            os.getenv('GALAXY_SLOTS'),
            os.getenv('GALAXY_SLOTS_CONFIGURED') is not None)
        if galaxy_slots:
            self.multithreading_level = galaxy_slots
                
    def parse_env_config (self, env_string):
        """Parse a MIMODD_CONFIG_UPDATE string yielding param, value pairs."""

        for setting in env_string.split(':'):
            try:
                param, value = setting.split('=') 
            except ValueError:
                raise ConfigParseError(
                    'Bad format of $MIMODD_CONFIG_UPDATE. \
Expected specifications of type "PARAM=VALUE". Got "{0}".', setting)
            yield param, value
    
    def adjust_galaxy_slots (self, galaxy_slots, galaxy_slots_configured):
        # Galaxy uses a default of "1" for GALAXY_SLOTS
        # if no value was specifed through the job runner.
        # to distinguish the default "1" (which we want to ignore)
        # from an explicitly requested "1" (which should be respected)
        # we can look at GALAXY_SLOTS_CONFIGURED, which is only set in the
        # second case. This environmental variable is currently
        # undocumented (communicated by John Chilton), we use it only
        # when GALAXY_SLOTS == "1", but do not generally rely on it.
        if galaxy_slots:
            try:
                galaxy_slots = int(galaxy_slots)
            except ValueError:
                return None
            if galaxy_slots > 1 or (galaxy_slots == 1 and
                                    galaxy_slots_configured):
                return galaxy_slots

    def update_settings (self, new_settings, verbose = False):
        """Update the Config instance based on a param: value mapping.

        Return True if the operation caused a change to the instance,
        False otherwise."""
        
        config_changes = False
        for param, value in new_settings.items():
            if param.lower() not in self._configurable_params:
                raise ConfigParseError('Unknown config parameter "{0}".',
                                       param, value)
            if param.lower() in self._path_params:
                value = os.path.abspath(os.path.expanduser(value))
            old_value = getattr(self, param.lower())
            T = type(old_value)
            try:
                value = T(value)
            except (ValueError, TypeError):
                message = 'Expected value of type ' + T.__name__ + \
                          ' for parameter {0}.'
                raise ConfigParseError(message, param, value)
            if value != old_value:
                config_changes = True
                setattr(self, param.lower(), value)
        return config_changes                

    def parse_cfg_param_line (self, line):
        """Parse a parameter, value pair from a single config file line."""
        
        try:
            param, value = [_.strip() for _ in line.split('=')]
        except ValueError:
            raise ConfigParseError('Expected PARAM = VALUE format.',
                                   line.strip())

        return param, value
                
    def update_cfg_line (self, line):
        """Change a config file line to the corresponding setting of this instance."""
        
        if line.strip() and line[0] != '#':
            param, value = self.parse_cfg_param_line(line)
            if param in self._configurable_params:
                current_value = getattr(self, param)
                line = '{0} = {1}\n'.format(
                        param, "r'{0}'".format(current_value) if isinstance(
                        current_value, str) else current_value)
        return line

    def write_config (self):
        """Update the config file with the settings of the Config instance."""
        
        # read current config file
        with open(self._cfg_path, 'r') as cfg_file:
            old_config = cfg_file.readlines()
        # write new config file
        cfg_file = open(self._cfg_path, 'w')
        try:
            for line_no, line in enumerate(old_config):
                try:
                    new_line = self.update_cfg_line(line)
                except ConfigParseError as e:
                    e.message = 'Error in config file at line ' + \
                                str(line_no) + ': "{0}".\n' + \
                                e.message
                    raise
                cfg_file.write(new_line)
            cfg_file.close()
        except:
            cfg_file.close()
            # restore old config file version
            with open(self._cfg_path, 'w') as cfg_file:
                for line in old_config:
                    cfg_file.write(line)
            raise

    def display_config (self, title = 'current MiModD settings'):
        """Print a report of the current settings."""
        
        print ()
        print (title.upper())
        print ('-' * len(title))
        print ('PARAMETER : VALUE')
        print ('.' * len(title))

        for param in self._configurable_params:
            print ('{0} : {1}'.format(param.upper(), getattr(self, param)))

config_object = Config()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(usage = argparse.SUPPRESS,
                                     formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description = """

view and modify configuration settings:

run without options to view current settings or
use the optional arguments below to change specific settings
(requires write access to the MiModD configuration file
in the installation directory).
""")
    parser.add_argument('--tmpfiles', '--tmpfiles-path', metavar = 'PATH', dest = 'tmpfiles_path', default = argparse.SUPPRESS, help = 'change the directory that MiModD will use to store temporary files')
    parser.add_argument('--snpeff', '--snpeff-path', metavar = 'PATH', dest = 'snpeff_path', default = argparse.SUPPRESS, help = "change the directory of your system's SnpEff installation")
    parser.add_argument('-t', '--threads', '--multithreading-level', dest = 'multithreading_level', default = argparse.SUPPRESS, help = 'change the maximal number of threads that any MiModD tool is allowed to use by default')
    parser.add_argument('-m', '--memory', '--max-memory', dest = 'max_memory', default = argparse.SUPPRESS, help = 'change the maximal memory in GB that any MiModD tool is allowed to use by default (will not affect the snap tool)')
    args = vars(parser.parse_args())
    if args:
        if config_object.update_settings(args):
           config_object.write_config()
    print()
    print ('Settings for package MiModD in:', os.path.dirname(config_object.__file__), end = '')
    config_object.display_config (title = '                       ')
else:
    # do not attempt this when __name__ == '__main__' on Python 3.3
    sys.modules[__name__] = config_object
