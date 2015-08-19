'''
Created spring 2015

@author: martin.melchior
'''
import os
import imp
from euclidwf.framework.taskdefs import Package
from euclidwf.utilities.error_handling import ConfigurationError
import sys

class TaskProperties(object):
    
    def __init__(self, executable, package, **kwargs):
        self.executable=executable
        self.package=package
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
                
    def __hash__(self):
        return hash(self.executable)+hash(self.package)
    
    def __eq__(self, other):
        if not isinstance(other, TaskProperties):
            return False
        if set(self.__dict__.keys()) != set(other.__dict__.keys()):
            return False
        for k,v in self.__dict__.iteritems():
            if v!=other.__dict__[k]:
                return False
        return True

    def __neq__(self,other):
        return not self.__eq__(other)


class PackageSource(object):
    
    def __init__(self, pkgname, pkgrepos, pkgversion=None):
        self.pkgname=pkgname
        self.pkgrepos=pkgrepos
        self.pkgversion=pkgversion

    def __eq__(self, other): 
        if not isinstance(other,PackageSource):
            return False
        return self.pkgname == other.pkgname and \
                self.pkgversion == other.pkgversion and \
                self.pkgrepos == other.pkgrepos                
                
    def __neq__(self, other): 
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.pkgname)+hash(self.pkgversion)
    
    def __repr__(self):
        return "Package: name=%s, version=%s"%(self.pkgname,self.pkgversion)
    

PACKAGE_REPOSITORIES={}

def load_pkgrepos(repospath, reload_repos=False):
    reposname=resolve_reposname(repospath)
    if reposname in PACKAGE_REPOSITORIES.keys() and not reload_repos:
        return PACKAGE_REPOSITORIES[reposname]
    pkgrepos=PackageRepository(repospath)
    PACKAGE_REPOSITORIES[reposname]=pkgrepos
    return PACKAGE_REPOSITORIES[reposname]
    
    
class PackageRepository(object):

    def __init__(self, repospath):
        self.repospath=repospath
        self.reposname=resolve_reposname(repospath)
        self.packages={} # pkgname : Package
        self.load()
    
    
    def load(self):
        for filename in os.listdir(self.repospath):
            pkgfile= os.path.join(self.repospath,filename)
            _name,_ext = os.path.splitext(pkgfile)
            if os.path.isfile(pkgfile) and _ext==".py":
                try:
                    self._load_packages(pkgfile)
                except:
                    pass # just ignore
            

    def _load_packages(self, pkgfile):
        filename=os.path.basename(pkgfile)
        module_name,_=os.path.splitext(filename)
        if module_name in sys.modules.keys():  
            del sys.modules[module_name]
        _module=imp.load_source(module_name, pkgfile)
        for k,v in _module.__dict__.iteritems():
            if isinstance(v, Package):
                if k in self.packages.keys():
                    raise ConfigurationError("Multiple definitions of the same package (%s) found in package repository %s."%(k,self.repospath))                
                self.packages[v.pkgname]=v

        
def resolve_reposname(repospath):
    return os.path.basename(repospath) 


