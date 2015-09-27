
import os, sys, subprocess, time, random, tempfile
from glob import glob
from bl.dict import Dict

"""There are other queue libraries; this one implements a simple file-based synchronous queue 
that is processed at set intervals by the queue process.
"""

class Queue(Dict):

    def __init__(self, path, log=print, debug=False):
        Dict.__init__(self, path=path, log=log, debug=debug)

    def __repr__(self):
        return "%s(path='%s')" % (self.__class__.__name__, self.path)

    def listen(self, sleep=10):
        """listen to the queue directory, with a wait time in seconds between processing"""
        while True:
            self.process()
            time.sleep(sleep)

    def insert(self, script, prefix=""):
        """insert the given script into the queue"""
        qfn = os.path.join(
            self.path,
            "%s-%.5f-%.5f" % (prefix, time.time(), random.random()))
        qf = open(qfn, 'wb')
        qf.write()
        qf.close()
        return qfn

    def list(self, pattern="*"):
        """get a list of files currently in the queue."""
        return [fn for fn in 
                glob(os.path.join(self.path, pattern))
                if os.path.basename(fn)[0] != '!']

    def process(self):
        """process the items in the queue that are ready."""
        fns = [fn for fn in self.list() 
                if os.path.basename(fn)[0]!='!']
        for fn in fns:
            stderr = tempfile.NamedTemporaryFile()
            self.log("[%s] %s" % (log.timestamp(), fn))
            try:
                result = subprocess.check_call(
                    [fn], universal_newlines=True, stderr=stderr)
                if result != 0:
                    newfn = self.rename(fn, prefix="!")
                    self.log("result!=0:", newfn)
                elif self.debug==True:
                    self.rename(fn, prefix="!_")
                else:
                    os.remove(fn)
            except subprocess.CalledProcessError as exception:
                # rename the script file to suppress further execution attempts
                newfn = self.rename(fn, prefix="!")
                self.log("CalledProcessError:", newfn, sys.exc_info()[1])
                self.handle_script_exception(scriptfn=newfn, errorfn=stderr.name)

    def handle_script_exception(self, scriptfn=None, errorfn=None):
        """handles exceptions that occur during queue script execution.
        Default script exception handling:
            * put the traceback into a file named scriptfn+".ERR" 
                (scriptfn has already been renamed with !)
            * also put the traceback into the queue log
        Override this method for custom exception handling. Named parameters that are given:
            scriptfn = the filesystem path to the queue script file
            errorfn  = the filesystem path to the traceback file
        """
        if errorfn is not None and os.path.exists(errorfn):
            errorf = open(errorfn, 'rb')
            t = errorf.read(); errorf.close()
            errorf = open(scriptfn+'.ERR', 'wb')
            errorf.write(t); errorf.close()
            if os.path.normpath(errorfn) != os.path.normpath(scriptfn+'.ERR') \
            and os.path.exists(errorfn):
                os.remove(errorfn)
        self.log(t)

    def rename(self, fn, prefix="!"):
        newfn = os.path.join(
            self.path,
            prefix + os.path.basename(fn))
        os.rename(fn, newfn)
        return newfn
