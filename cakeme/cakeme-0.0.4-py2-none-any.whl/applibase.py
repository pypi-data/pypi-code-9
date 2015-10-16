from collections import namedtuple
import logging
import shlex
import os
import subprocess

ProcessValues = namedtuple("ProcessValues", "return_code out err")

def setUpLogging(destination='/var/tmp/myapp.log'):
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler(destination)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

class ApplicationBase:
    APP_NAME = ""
    LOGFILE = ""
    RESULT = ProcessValues(-1, "", "")

    def __init__(self, app_name, result_directory):
        self.logger = setUpLogging(os.path.join(result_directory,"{}.{}".format(app_name,"log")))
        self.APP_NAME = app_name

    def executeCommand(self,command):
        self.logger.info("Running {}".format(command))
        cmd = shlex.split(command)
        try:
            process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
            out, err = process.communicate()
            self.RESULT = ProcessValues(process.returncode, out, err)
            return self.RESULT
        except OSError as e:
            self.logger.error("test {}".format(str(e)))

    def logResults(self):
        self.logger.info("{} : {}".format(self.APP_NAME,self.RESULT.out))
        #self.logger.error("{} : {}".format(self.APP_NAME, self.RESULT.err))

    def run(self):
        pass
