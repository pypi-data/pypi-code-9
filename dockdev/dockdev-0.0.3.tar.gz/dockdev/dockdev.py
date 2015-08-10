#!/usr/bin/env python

import subprocess, pystache, tempfile, yaml, blessings, collections, platform, os, argparse

from blessings import Terminal
term = Terminal()


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__)) 

class App:
    def __init__(self, name, config):
        self.name = name
        self.__dict__.update(config)
        
    def get_commit(self, branch = 'master'):
        cmd = ['git', 'ls-remote', self.git, branch]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out == '':
            raise Exception('Branch not found')
        if err:
            raise Exception(err)
        return out.rstrip().split('\t')[0]
        
    def get_tpl(self, input):
        return {
            'tag' : 'dev' if input == 'dev' else self.get_commit(input),
            'host' : get_docker_host(),
            'dir' : os.path.abspath(os.path.join("./", 'development-environment', self.dir)),
            'dev' : input == 'dev'
        }
           
def get_config(config_filename):
    try:
        with open(config_filename, 'r') as config_file:
            data = yaml.safe_load(config_file)
            return data['config'], [ App(name, values) for name, values in data['apps'].iteritems() ]
    except IOError:
        raise Exception("Could not read config")
           
def get_template(template_filename):
    try:
        with open(template_filename, 'r') as input_file:
            return input_file.read()
    except IOError:
        raise Exception("Could not read template file")

def get_docker_host():
    if platform.system() == 'Darwin':
        p = subprocess.Popen(['boot2docker', 'ip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out.strip()
    else:
        return 'localhost'



def main():    
    parser = argparse.ArgumentParser(description='DevTool')
    parser.add_argument('--config', help='Specifies the config file. Defaults to apps.yml.', default="./apps.yml")
    parser.add_argument('--template', help='Specifies the template file. Defaults to docker-compose.yml.tpl', default='./docker-compose.yml.tpl')
    parser.add_argument('--prefix', help='Specifies the prefix. Defaults to configured parameter', default=None)
    parser.add_argument('remainder', nargs=argparse.REMAINDER, help='You can specify mappings positionally, e.g. App1:Version2 App2:Version2')
    args = parser.parse_args()
    
    config, apps = get_config(args.config)
    template = get_template(args.template)
    
    try:
        provided_versions = dict( tuple(app.split(':')) for app in args.remainder )
    except ValueError:
        raise Exception("Arguments must be in the following format: App1:Version2 App2:Version2")
    
    print 
    print "----------------------------------------"
    print "Set Up Dev Environment"
    print "----------------------------------------"
    print 
    print "Press ENTER for master, type dev for build from source:"
    print 

    # some useful globals
    tpl = {
        'maven_cache' : os.path.join(os.path.expanduser("~"), '.m2'),
        'sbt_cache' : os.path.join(os.path.expanduser("~"), '.sbt'),
        'ivy2_cache' : os.path.join(os.path.expanduser("~"), '.ivy2')
    }
    
    for app in apps:
        if app.name not in provided_versions:
            version = raw_input("%s? [master]: " % app.name)
            if version == '':
                version = 'master'
        else:
            print # nothing
            version = provided_versions[app.name]

        tpl[app.name] = app.get_tpl(version)
        print(term.move_up() +"%s = %s " % (app.name, tpl[app.name]['tag']) + term.clear_eol())


    if args.prefix:
        prefix = args.prefix
    else:
        prefix = config['default_prefix']
        
    output_dir = os.path.join(tempfile.mkdtemp(), prefix)
    os.mkdir(output_dir)
    
    output_yml = pystache.render(template, tpl)
    with open(os.path.join(output_dir, config['file']), 'w') as output_file:
        output_file.write(output_yml)

    print 
    print "Run this:"
    print
    print "export %s=\"%s\"" % (config['env_file'], output_file.name)
    print "export %s=\"%s\"" % (config['env_prefix'], prefix)
    print


if __name__ == "__main__":
    main()

    
    
