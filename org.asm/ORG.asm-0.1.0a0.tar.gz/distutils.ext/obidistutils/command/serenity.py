'''
Created on 16 août 2015

@author: coissac
'''

from distutils.core import Command
import os.path
import glob
from obidistutils.serenity.rerun import enforce_good_python
from builtins import None

class serenity(Command):
    '''
    Install the package in serenity mode
    '''
    
    description = "Install the package in serenity mode"

    user_options = [
        ('virtualenv', None,
         "Name of the virtualenv")]
    

    def initialize_options (self):
        self.virtualenv = None
        self.minversion = None
        self.maxversion = None
        self.fork       = None

    def finalize_options (self):
        package = self.distribution.metadata.get_name()
        version = self.distribution.metadata.get_version()
        
        if self.virtualenv is None:
            self.virtualenv="%s-%s" % (package,version)
            
        if self.minversion is None:
            self.minversion="3.4"
            
        if self.fork is None:
            self.fork="3.4"
        
            

    def run (self):
        enforce_good_python(minversion, maxversion, fork)
    
        local_serenity.append(True)
        serenity_snake(args.virtual,package,version)

        if (install_requirements(requirementfile)):
            rerun_with_anothe_python(sys.executable,minversion,maxversion,fork)
        
        try:
            check_requirements(requirementfile)
        except RequirementError as e :
            log.error(e)                                   
            sys.exit(1)
    

        if self.distribution.serenity:
            self.install_doc = os.path.join(self.install_doc,"../export/share")
            self.install_doc=os.path.abspath(self.install_doc)
            self.mkpath(self.install_doc)
            self.mkpath(os.path.join(self.install_doc,'html'))
            outfiles = self.copy_tree(os.path.join(self.build_dir,'html'),  # @UnusedVariable
                                      os.path.join(self.install_doc,'html'))
                
            self.mkpath(os.path.join(self.install_doc,'man','man1'))
            outfiles = self.copy_tree(os.path.join(self.build_dir,'man'),  # @UnusedVariable
                                      os.path.join(self.install_doc,'man','man1'))

            for epub in glob.glob(os.path.join(self.build_dir,'epub/*.epub')):
                self.copy_file(os.path.join(epub), 
                               os.path.join(self.install_doc,os.path.split(epub)[1]))
            
    def get_outputs(self):
        directory=os.path.join(self.install_doc,'html')
        files = [os.path.join(self.install_doc,'html', f) 
                 for dp, dn, filenames in os.walk(directory) for f in filenames]  # @UnusedVariable
        
        directory=os.path.join(self.build_dir,'man')
        files.append(os.path.join(self.install_doc,'man','man1', f) 
                 for dp, dn, filenames in os.walk(directory) for f in filenames)  # @UnusedVariable

        directory=os.path.join(self.build_dir,'epub')
        files.append(os.path.join(self.install_doc, f) 
                 for dp, dn, filenames in os.walk(directory)  # @UnusedVariable
                 for f in glob.glob(os.path.join(dp, '*.epub')) )
        
        return files
