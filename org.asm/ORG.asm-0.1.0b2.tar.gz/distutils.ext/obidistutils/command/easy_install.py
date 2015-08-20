'''
Created on 15 août 2015

@author: coissac
'''

try:
    from setuptools.command.easy_install import easy_install as easy_install_ori
    
    class easy_install(easy_install_ori):
        
        def install_egg_scripts(self, dist):
            """Write all the scripts for `dist`, unless scripts are excluded"""
            if not self.exclude_scripts and dist.metadata_isdir('scripts'):
                for script_name in dist.metadata_listdir('scripts'):
                    if dist.metadata_isdir('scripts/' + script_name):
                        # The "script" is a directory, likely a Python 3
                        # __pycache__ directory, so skip it.
                        continue
                    self.install_script(
                        dist, script_name,
                        dist.get_metadata('scripts/' + script_name)
                    )
            self.install_wrapper_scripts(dist)

    
except ImportError:
    pass 