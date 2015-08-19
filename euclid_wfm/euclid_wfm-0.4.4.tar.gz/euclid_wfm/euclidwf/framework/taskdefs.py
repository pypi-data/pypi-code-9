'''
Created on Apr 25, 2015

@author: martin.melchior
'''

class Package():
    def __init__(self, pkgname, executables=[]):
        self.pkgname=pkgname
        self.executables=executables
        
    def __repr__(self):
        return "PACKAGE %s"%self.pkgname    
    
class ComputingResources():
    def __init__(self, num_cores=1, ram=1.0, walltime=1.0):
        self.num_cores=num_cores
        self.ram=ram
        self.walltime=walltime
        
    def __repr__(self):
        return "CORES=%s | RAM=%s | WALLTIME=%s"%(self.num_cores, self.ram, self.walltime)

class Executable():
    def __init__(self, execname, inputs=[], outputs=[], resources=ComputingResources()):
        self.execname=execname
        self.inputs=inputs
        self.outputs=outputs
        self.resources=resources
    
MIME_XML="xml"
MIME_TXT="txt"
TYPE_FILE="file"
TYPE_LISTFILE="listfile"

class Input():
    def __init__(self, inputname, dm_type=None, content_type=TYPE_FILE):
        self.name=inputname
        self.dm_type=dm_type

class Output():
    def __init__(self, outputname, dm_type=None, mime_type=MIME_XML, content_type=TYPE_FILE):
        self.name=outputname
        self.dm_type=dm_type
        self.mime_type=mime_type
        self.content_type=content_type
        
 
