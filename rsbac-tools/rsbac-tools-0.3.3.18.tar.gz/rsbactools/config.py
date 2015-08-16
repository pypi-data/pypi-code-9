import os
import sys
import re
import json
from configparser import ConfigParser


import logging
logging.basicConfig(format='%(levelname)s:%(name)s: %(message)s')
log = logging.getLogger(__name__)


try:
    from rsbactools import which
except ImportError as error:
    print(error)
    sys.exit(-1)


class JsonLoader(object):
    """Class to load a json file with error handling."""

    def __init__(self):
        self.config_values = None
        self.config_file = None

    def set_log_level(self, log_level):
        log.setLevel(log_level) 

    def add_config(self, config_file):
        if os.path.isfile(config_file):
            self.config_file = config_file
            return True
        else:
            log.warning("FileNotFound: %s" % config_file)
            return False

    def load_config(self):
        if not self.config_file:
            return False
        try:
            with open(self.config_file) as fd:
                self.config_values = json.loads(fd.read())
            return True
        except ValueError as error:
            log.warning("%s in %s" % (error, self.config_file))
            return False

    def get_values(self):
        return self.config_values


class IniLoader(object):
    """ini parser callback"""

    def __init__(self, config_name):
        self.config_name = config_name

    def parse_config(self):
        """parser the config"""
        try:
            cp = ConfigParser.read(self.config_file)
            values = cp.__dict__['_sections'].copy()
            return values
        except Exception as error:
            log.info(error)


class JailParser(object):
    """ 
    Read the jailconfig from adamantix style which are placed 
    in /etc/rsbac/jail and return a dictonary with six parts.
    (c) 2008-2011 Jens Kasten <igraltist@rsbac.org>
    """

    def __init__(self, config_path="/etc/rsbac/jail"):
        # path to jail configuration files
        self.jail_config_path = config_path
        # dictionary to keep jail information
        # it has the same layout like a jail configuration file 
        # the values for jail-flags, max-caps, scd-read, scd-modify
        # would be overriden if values found in configuration file 
        # through a list
        self.jail_parts = {
            'jail-chroot': '',
            'jail-ip': '',
            'jail-flags': 0, 
            'max-caps': 1,
            'scd-read': 2,
            'scd-modify': 3,
        }
        # collect absolute path for binaries
        self.ifconfig = which("ifconfig")
        self.route = which("route")
    
    def check_config_path(self, config):
        """Return the absolute path if jail configuration file exists. """
        config = os.path.join(self.jail_config_path, config)
        if os.path.isfile(config):
            return config 
        else:
            print("Could not found jail configuration file '%s'." % config)
            sys.exit()

    def __call__(self, config):
        """Make it callable."""
        line = []
        start = []
        end = []
        values = []
        
        config = self.check_config_path(config)
        with open(config, "r") as fd:
            for i in fd:
                # remove comments and whitespace
                i = i.replace("\n", "")
                if re.search(';', i):
                    temp_line = i.split(";")[0]
                    if len(temp_line) > 1:
                        line.append(temp_line.strip())
                else: 
                    line.append(i.strip())
        
        # remove empty elements from line list                
        line = [i for i in line if len(i) >= 1]
        for i in range(len(line)):
            if re.search('^"', line[i]) and re.search('"$', line[i]):
                if len(line[i]) == 1:
                    print("This sign \" is not allow as standalone.")
                    print("For comments use sign ;")
                    print("Please edit your configfile, '%s'" % config)
                    sys.exit()
                else:
                    if i == 0:
                        chroot_dir = line[i].replace('"', '')
                        if os.path.isdir(chroot_dir) or len(chroot_dir) == 0:
                            self.jail_parts['jail-chroot'] = line[i].replace('"', '')
                        else:
                            print("Path does not exists %s." % chroot_dir)
                            sys.exit()
                    elif i == 1:
                         ip = line[i].replace('"', '')
                         self.jail_parts['jail-ip'] = self.check_ip(ip, config)
            # this part search for ( and ) on which place they are in list line
            if re.search('\(', line[i]):
                start.append(i)
                line[i] = line[i].replace('(', '').replace(' ', '')
            if re.search('\)', line[i]):
                end.append(i)
                line[i] = line[i].replace(')', '').replace(' ', '')
        if len(start) < len(end):
            print("Missing open '(' in '%s'." % (config))
            sys.exit(1)
        elif len(start) > len(end):    
            print("Missing close ')' in '%s'." % (config))
            sys.exit(1)
        elif len(start) < 4 and len(end) < 4:
            print("Missing on category '()' in '%s'." % config)
            sys.exit(1)
        elif len(start) > 4 and len(end) > 4:
            print("One category '()' is to much in '%s'." % config)
            sys.exit(1)
        # the start and end can only contain 4 elements
        # the values between start and end must be add as categories values
        i = 0
        while i < 4:
            for key, value in self.jail_parts.items():
                if i == value:
                    if start[i] == end[i]:
                        if len(line[start[i]]) == 0:
                            self.jail_parts[key] = line[start[i]]
                        else:
                            # even if is a string, add is as list
                            # for this :start[i]+1
                            self.jail_parts[key] = line[start[i]:start[i]+1]
                    else:
                        self.jail_parts[key] = line[start[i]:end[i]+1]
                        # wehn the list have empty entries remove it
                        for k in self.jail_parts[key]:
                            if len(k) == 0:
                                self.jail_parts[key].remove(k)
            i += 1               
        return self.jail_parts

    def check_ip(self, ip, config):
        """Check ip part."""
        ip_default = "0.0.0.0"
        ip_localhost = "127.0.0.1"
        if len(ip) == 0:
            return ip_default 
        elif ip == "lo" or ip == "localhost":
            return ip_localhost 
        else:
            if self.check_ip_format(ip):
                return ip
            else:
                ip_from_interface = self.check_interface(ip)
                if ip_from_interface:
                    return ip_from_interface
                else:
                    print("Given network interface '%s' is no up in '%s'." % (ip, config))
                    return ip

    def check_ip_format(self, ip):
        """Valided the ip address."""
        ip_pattern = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        ip_pattern += "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        ip_pattern += "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        ip_pattern += "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        if re.compile(ip_pattern).match(ip):
            return True
        else:
            return False

    def check_interface(self, interface):
        ip = []
        cmd = [self.ifconfig, interface]
        try:
            # env must set to obtain english words for searching key
            result = Popen(cmd, stdout=PIPE, stderr=PIPE, env={"LC_ALL":"C"})
            result.wait()
            if result.returncode == 0:
                ip = result.communicate()[0].strip()
                ip = re.findall("inet addr:(\d+\.\d+\.\d+\.\d+)" , ip)
                if len(ip) > 0:
                    return ip[0]
        except OSError as e:
            print(str(e[1]))
        except IOError as e:
            print(str(e[1]))


# Parser to get content from a configfile.
#
# config file syntax:
#       key = value
#       #key = value    <- commented 
#       key = value  # comment
#
"""
(c) 2007-2012 Jens Kasten <jens@kasten-edv.de>
"""

class Parser(object):
    """Simple config parser for key value configuration file."""
   
    def __init__(self, config_name):
        self.config_name = config_name

    def _check_config_syntax(self):
        """Return a cleaned dictionary from a befor readed config file."""
        print(self.config_name)
        if not os.path.isfile(self.config_name):
            return False
        else:
            counter = 1
            config = []
            with open(self.config_name) as fd:
                lines = fd.readlines()
                # remove withespace but not and arguments 
                for line in lines:
                    if len(line) > 1 and not line.startswith('#'):
                        # split only the first equal sign form left side
                        temp = line.strip().split("=", 1)
                        assert len(temp) == 2, "Missing sign '=' in %s on line %s" %  (self.config_name, counter)
                        # remove all withespace from string
                        key = re.sub(r'\s', '', temp[0])
                        assert len(temp) == 2, "Missing value in %s on line %s" % (self.config_name, counter)
                        # remove comment
                        value = temp[1].split("#")[0].strip()
                        content = "=".join([key, value])
                        config.append(content)
                    counter += 1
            return config

    def parse_config(self):
        """Return a dictionary"""
        lines = self._check_config_syntax()
        if not lines:
            return 
        config = {}
        for line in lines:
            if len(line) > 0:
                line = line.split("=", 1)
                config[line[0]] = line[1]
        return config
