'''
Created on Apr 25, 2015

@author: martin.melchior
'''
import argparse
import imp
import inspect
import os
import sys

from euclidwf.framework import taskdefs, taskprops


PREFIX='proxy_functions'

def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Utility for generating proxy functions for executables to be used in the pipeline specifications.")
    parser.add_argument("--pkgdefs", help="Path to folder that contains the package definitions (package repository).")
    parser.add_argument("--destdir", help="Directory to write the wrappers to.", required=False)
    args = parser.parse_args()
    
    return args


def _packages_definitions(module):
    pkgs=[]
    for _name,_obj in inspect.getmembers(sys.modules[module.__name__]):
        if isinstance(_obj,taskdefs.Package):
            pkgs.append(_obj)
    return pkgs


def _find_execs(pkgfile):
    pkg_module_name,_=os.path.splitext(pkgfile)
    pkg_module=imp.load_source(pkg_module_name, pkgfile)
    pkgdefs = _packages_definitions(pkg_module)
    if len(pkgdefs)>1:
        raise ValueError("Definitions for more than one package found in the package definition file %s."%pkgfile)  
    if len(pkgdefs)==0:
        return None, None
    pkg=pkgdefs[0]
    return pkg.pkgname, pkg.executables


def _load_pkg_defs(source_files):
    pkgs={}
    for source_file in source_files:
        pkgname,execs=_find_execs(source_file)
        if pkgname in pkgs.keys():
            raise ValueError("Package %s seems to be defined in more than one package definition file."%pkgname)
        pkgs[pkgname]=(execs, source_file)
    return pkgs


def _pkgpath(pkgname):
    return pkgname.replace(".","/")

def _pkg_file_name(pkgname):
    return "__init__.py"

def _inputnames(_exec):
    return tuple([_input.name for _input in _exec.inputs])

def _outputnames(_exec):
    return tuple([_output.name for _output in _exec.outputs])

def _add_init_files(rootdir):
    for root, _, files in os.walk(rootdir):
        if root != rootdir and '__init__.py' not in files:
            with open(root+"/__init__.py","w"):
                pass


def main():
    args = parse_cmd_args()
    generate_proxyfcts(args.pkgdefs, args.destdir)


def generate_proxyfcts(pkgrepospath, destdir):
    pkgrepos = taskprops.load_pkgrepos(pkgrepospath)
    pkgs = pkgrepos.packages
    
    for pkgname,pkg in pkgs.iteritems():
        mod_pkgname="%s_%s"%(PREFIX,pkgname)
        relpkgpath=_pkgpath(mod_pkgname)
        abspkgpath=os.path.join(destdir, relpkgpath)
        if not os.path.exists(abspkgpath):
            os.makedirs(abspkgpath)
        pkg_wrapper_path=os.path.join(abspkgpath, _pkg_file_name(pkgname))
        with open(pkg_wrapper_path, "w") as pkg_wrapper_file:
            pkg_wrapper_file.write(PROXY_FCT_FILE_TEMPLATE%(pkgname,pkgrepospath, None))
            for _exec in pkg.executables:
                inputnames=_inputnames(_exec)
                outputnames=_outputnames(_exec)
                pkg_wrapper_file.write(PROXY_FCT_TEMPLATE%(_exec.execname, inputnames, outputnames, _exec.execname))
    _add_init_files(destdir)


PROXY_FCT_FILE_TEMPLATE=\
'''
\'''
Proxy functions code needed for defining pipeline dataflow.
Generated from package definition file(s). 
Version: 0.1
\''' 
from euclidwf.framework.workflow_dsl import invoke_task
from euclidwf.framework.taskprops import TaskProperties, PackageSource

pkgsource=PackageSource(pkgname='%s', pkgrepos='%s', pkgversion='%s')

'''

PROXY_FCT_TEMPLATE=\
'''
def %s(**kwargs):
    inputnames=%s
    outputnames=%s
    execname='%s'
    props=TaskProperties(executable=execname,package=pkgsource)
    return invoke_task(props, inputnames, outputnames, **kwargs)

'''
   

if __name__ == '__main__':
    main()
