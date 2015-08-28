import os
import shutil
import argparse
import subprocess

module_templates = [
    'python',
    'matlab',
    ]

class create_bisque_module(object):
    desc = 'module operations: register, unregister'
    def __init__(self, version):
        parser = argparse.ArgumentParser("create a bisque module")
        parser.add_argument('module_type')
        parser.add_argument('module_name')

        self.args = parser.parse_args()
        print self.args.module_type , self.args.module_name
        if self.args.module_type not in module_templates:
            parser.error("unsupported bisque module type: supported types %s" % ",".join(module_templates))

    def run(self):
        subprocess.call (['pcreate', '-s', '%s_module' % self.args.module_type, self.args.module_name])
        if not os.path.exists ('modules'):
            os.makedirs ('modules')
            print "creating modules directory"
        shutil.move("%s/%s" % (self.args.module_name, self.args.module_name.lower()), 'modules')
        shutil.rmtree (self.args.module_name)

