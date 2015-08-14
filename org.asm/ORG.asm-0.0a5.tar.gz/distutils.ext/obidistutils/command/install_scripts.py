'''
Created on 20 oct. 2012

@author: coissac
'''
from distutils.command.install_scripts import install_scripts as ori_install_scripts

import os.path
from distutils import log

class install_scripts(ori_install_scripts):

    def initialize_options(self):
        ori_install_scripts.initialize_options(self)
        self.public_dir = None
                        
                    
    def install_public_link(self):
        self.mkpath(self.public_dir)
        for file in self.get_outputs():
            if self.dry_run:
                log.info("changing mode of %s", file)
            else:
                log.info("exporting file %s -> %s", file,os.path.join(self.public_dir,
                                        os.path.split(file)[1]
                                        ))
                dest = os.path.join(self.public_dir,
                                    os.path.split(file)[1]
                                   )
                if os.path.exists(dest):
                    os.unlink(dest)
                os.symlink(file,dest)
                    


    def run(self):
        ori_install_scripts.run(self)
        if self.distribution.serenity:
            self.public_dir=os.path.join(self.install_dir,"../export/bin")
            self.public_dir=os.path.abspath(self.public_dir)
            self.install_public_link()


