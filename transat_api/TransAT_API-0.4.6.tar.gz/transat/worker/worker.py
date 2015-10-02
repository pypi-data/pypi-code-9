import uuid
import os.path
import subprocess as sp
import logging
import sys

logger = logging.getLogger(__name__)

"""
.. module:: Worker
   :platform: Unix, Windows
   :synopsis: Defines workers that are able to execute tasks

.. moduleauthor:: ASCOMP <info@ascomp.ch>


"""


class Worker(object):
    def __init__(self, name='local'):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        self.name = name

    def run_cmd(self, cmd, wd):
        file_name = os.path.join(wd, "sim.log")
        logger.info("run_cmd:" + str(" ".join(cmd)) + ", in wd:" + str(wd))
        try:
            p = sp.Popen(cmd, stdout=open(file_name, 'wb'), stderr=sp.PIPE, cwd=wd)
            stdout, stderr = p.communicate()
            if stderr:
                logger.error(stderr)
                print "Error in Worker running "+str(cmd)+" in "+str(wd)+". Error message is "+str(stderr)
                #sys.exit()
                #raise Exception #  TODO: On windows this throw an error even in a normal run
            logger.info("Done run_cmd:" + str(" ".join(cmd)) + ", in wd:" + str(wd))
        except KeyboardInterrupt:
            logger.info("Execution has been interrupted by the user (KeyboardInterrupt)")
            print "interrupting"

    def remove_file(self, filename, wd):
        filename = os.path.join(wd, filename)
        if os.path.exists(filename):
            os.remove(filename)

    def prepare_simulation_files(self, cmd, project_name, wd):
        cmd.append(project_name)
        return self.run_cmd(cmd, wd)

    def execute(self, task):
        print "Executing command: " + task.cmd

