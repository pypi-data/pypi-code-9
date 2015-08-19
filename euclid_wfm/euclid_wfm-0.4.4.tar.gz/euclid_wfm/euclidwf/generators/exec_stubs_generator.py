'''
Created on Apr 25, 2015

@author: martin.melchior
'''
import argparse
import inspect
import os
import shutil
import stat
import sys

from euclidwf.framework import taskdefs, taskprops
from euclidwf.framework.taskdefs import TYPE_LISTFILE
import pickle
from euclidwf.utilities import error_handling


def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Utility generating test stubs for executables.")
    parser.add_argument("--pkgdefs", help="Path to folder that contains the package definitions (package repository).")
    parser.add_argument("--destdir", help="Directory to write the test stubs to.")
    args = parser.parse_args()
    
    return args


class TestExec(object):
    
    def __init__(self, executable, package, attributes=None):
        self.executable=executable
        self.package=package
        self.attributes=attributes
        
    def execute(self, workdir, logdir, inputs, outputs, details=True):
        for outputname, reloutpath in outputs.iteritems():
            absoutpath=os.path.join(workdir,reloutpath)
            parentdir=os.path.dirname(absoutpath)
            if not os.path.exists(parentdir):
                os.makedirs(parentdir)
            with open(absoutpath,'w') as outfile:
                outfile.write("**************************************************************************\n")
                outfile.write("TEST STUB FOR %s - OUTPUT PORT: %s.\n"%(self.executable, outputname))
                outfile.write("**************************************************************************\n")
                outfile.write("Workdir: %s\n"%workdir) 
                outfile.write("Logdir: %s\n"%logdir) 
                outfile.write("Inputs:\n") 
                for inputname, relinpath in inputs.iteritems():
                    outfile.write("   (%s,%s)\n"%(inputname, relinpath))                 
                if details:
                    outfile.write("Details:\n") 
                    for inputname, relinpath in inputs.iteritems():
                        absinpath=os.path.join(workdir, relinpath)
                        with open(absinpath,'r') as infile:
                            _append_to_file(outfile, inputname, infile)


OUTPUTLISTLENGTH=3

class TestExecListOutput(object):
    
    def __init__(self, executable, package, attributes=None):
        self.executable=executable
        self.package=package
        self.attributes=attributes
        
    def execute(self, workdir, logdir, inputs, outputs, details=True):
        _,reloutpath=outputs.iteritems().next()
        workdir=os.path.abspath(workdir)
        listoutpath=os.path.join(workdir,reloutpath)
        parentdir=os.path.dirname(listoutpath)
        if not os.path.exists(parentdir):
            os.makedirs(parentdir)
        relpath,_=os.path.splitext(reloutpath)
        abspath =os.path.join(workdir,relpath)

        outputlist=[]
        for i in range(OUTPUTLISTLENGTH):
            outputlist.append("%s_%i"%(relpath,i+1))

        with open(listoutpath, "w") as listfile:
            pickle.dump(outputlist, listfile)
        
        for i in range(OUTPUTLISTLENGTH):        
            with open("%s_%i"%(abspath,i+1),'w') as outfile:
                outfile.write("**************************************************************************\n")
                outfile.write("TEST DATA SPLIT BY TEST STUB %s.\n"%self.executable)
                outfile.write("ELEMENT: %i\n"%(i+1))
                outfile.write("Referenced within the listfile %s.\n"%listoutpath)
                outfile.write("**************************************************************************\n")
                outfile.write("Workdir: %s\n"%workdir) 
                outfile.write("Logdir: %s\n"%logdir) 
                outfile.write("Inputs:\n") 
                for inputname, relinpath in inputs.iteritems():
                    outfile.write("   (%s,%s)\n"%(inputname, relinpath))                 
                    if details:
                        outfile.write("Details:\n") 
                        for inputname, relinpath in inputs.iteritems():
                            absinpath=os.path.join(workdir, relinpath)
                            with open(absinpath,'r') as infile:
                                _append_to_file(outfile, inputname, infile)


                
def _append_to_file(outfile, inputname, infile):
    outfile.write("    -------------------------------------\n")
    outfile.write("    Input (port: %s):\n"%inputname)
    outfile.write("    -------------------------------------\n")
    outfile.write("    -------------------------------------\n")
    for line in infile:
        outfile.write("        %s"%line)
        

def create_test_exec(pkgname, executable, outputpath, testexec='TestExec'):
    inputnames=tuple(["%s"%_input.name for _input in executable.inputs])
    outputnames=tuple(["%s"%_output.name for _output in executable.outputs])
    content=TEST_EXEC_TEMPLATE%("'%s'"%executable.execname, "'%s'"%pkgname, inputnames, outputnames, testexec)
    with open(outputpath, 'w') as outputfile:
        outputfile.write(content)
    os.chmod(outputpath, stat.S_IRWXU)
    

def _add_dependencies(destdir):
    src_path=inspect.getsourcefile(taskdefs)
    src_name=taskdefs.__name__
    copy_module(src_name, src_path, destdir)

    src_path=inspect.getsourcefile(taskprops)
    src_name=taskprops.__name__
    copy_module(src_name, src_path, destdir)

    src_path=inspect.getsourcefile(error_handling)
    src_name=error_handling.__name__
    copy_module(src_name, src_path, destdir)
    
    module=sys.modules[__name__]
    src_path=inspect.getsourcefile(module)
    src_name="euclidwf.generators.%s"%inspect.getmodulename(src_path)
    copy_module(src_name, src_path, destdir)
    
    for root, _, files in os.walk(destdir):
        if not '__init__.py' in files:
            with open(root+"/__init__.py","w"):
                pass


def copy_module(module_name, module_path, destdir):
    abspath=module_path
    relpath=module_name.replace(".", "/")+".py"
    destpath=os.path.join(destdir,relpath)
    dest_parent=os.path.dirname(destpath)
    if not os.path.exists(dest_parent):
        os.makedirs(dest_parent)
    shutil.copy2(abspath, destpath)


def check_output_for_list(_exec):
    list_outputs=filter(lambda o: o.content_type==TYPE_LISTFILE, _exec.outputs)
    if list_outputs and len(_exec.outputs)>1:
        raise ValueError("Not stub can be generated for executables that have more than one output \n"+ 
                            " and one of the outputs is a list.")
    else:
        return len(list_outputs)>0 
    

def main():
    args = parse_cmd_args()
    destdir = args.destdir
    pkgrepos = taskprops.load_pkgrepos(args.pkgdefs)
    pkgs = pkgrepos.packages
    for pkgname,pkg in pkgs.iteritems():
        for _exec in pkg.executables:
            execname=pkgname+"."+_exec.execname
            execpath=os.path.join(destdir, execname)            
            if os.path.isfile(execpath):
                raise RuntimeError("Files %s already exists."%execpath)
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            if check_output_for_list(_exec):
                create_test_exec(pkgname, _exec, execpath, 'TestExecListOutput')
            else:
                create_test_exec(pkgname, _exec, execpath)
    _add_dependencies(destdir)


TEST_EXEC_TEMPLATE=\
'''#!/usr/bin/env python
\'''
Test wrapper generated from package definition.
Version: 0.1
\''' 
import argparse
import os
from euclidwf.generators.exec_stubs_generator import TestExec, TestExecListOutput

execname=%s
pkgname=%s
inputnames=%s
outputnames=%s

def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Test Stub for Executable %%s."%%execname)
    parser.add_argument("--workdir", help="Workdir.", default=".")
    parser.add_argument("--logdir", help="Logdir.", default="./logdir")
    for inputname in inputnames:
        parser.add_argument("--%%s"%%inputname, help="Relative path to input (%%s) to tester."%%inputname)
    for outputname in outputnames:
        parser.add_argument("--%%s"%%outputname, help="relative path to output (%%s) to tester."%%outputname)
    args = parser.parse_args()    
    return args

def main():
    args = parse_cmd_args()
    tester=%s(execname, pkgname)
    inputs={}
    for inputname in inputnames:
        inputs[inputname]=getattr(args,inputname)
    outputs={}
    for outputname in outputnames:
        outputs[outputname]=getattr(args,outputname)
    tester.execute(args.workdir, args.logdir, inputs, outputs)


if __name__ == '__main__':
    main()

'''
   

if __name__ == '__main__':
    main()
