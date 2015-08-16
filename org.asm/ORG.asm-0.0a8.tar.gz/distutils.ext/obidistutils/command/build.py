'''
Created on 20 oct. 2012

@author: coissac
'''

from distutils.command.build import build as ori_build
from obidistutils.serenity.checksystem import is_mac_system


class build(ori_build):
    
    def has_ext_modules(self):
        return self.distribution.has_ext_modules()
    
    def has_pidname(self):
        return is_mac_system()

    def has_doc(self):
        return True
    
    
    sub_commands = [('pidname',has_pidname)
                   ] \
                   + ori_build.sub_commands + \
                   [('build_sphinx',has_doc)]
    
