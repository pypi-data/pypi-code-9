'''
Created on Apr 28, 2015

@author: martin.melchior
'''
import sys
import inspect
from euclidwf.framework import taskdefs, taskprops
from euclidwf.utilities.error_handling import ConfigurationError

def load_executable(taskname, pkgname, pkgrepos):
    if pkgname not in pkgrepos.packages.keys():
        raise ConfigurationError("Package with name %s not included in package repository (%s)."%(pkgname, pkgrepos.reposname))
    pkg=pkgrepos.packages[pkgname]
    execs=[_exec for _exec in pkg.executables if _exec.execname==taskname]
    if len(execs)==0:
        raise ConfigurationError("No executable with name %s found in package %s (package repos %s)."%(taskname, pkgname, pkgrepos.reposname))        
    return execs[0]


def _load_module(pkgname):
    if pkgname in sys.modules.keys():
        return sys.modules[pkgname]
    else:
        try:
            return __import__(pkgname, fromlist='*')
        except:
            raise 

    
def _package_instance(pkgmodule):
    pkgs=[]
    for _name,_obj in inspect.getmembers(sys.modules[pkgmodule.__name__]):
        if isinstance(_obj,taskdefs.Package):
            pkgs.append(_obj)
    if len(pkgs)==0:
        raise ValueError("Package %s not found.")
    elif len(pkgs)>1:
        raise ValueError("More than one Package with name %s found.")
    else:
        return pkgs[0]



if __name__ == '__main__':    
    taskname="vis_split_quadrants"
    pkgname="vis"
    pkgrepospath="/Users/martinm/Projects/euclid/pipeline_framework/prototype/wfm/trunk/euclidwf_examples/packages/pkgdefs"
    pkgrepos=taskprops.load_pkgrepos(pkgrepospath)
    e=load_executable(taskname, pkgname, pkgrepos)

    print e