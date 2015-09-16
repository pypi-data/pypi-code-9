'''
Created on Jun 5, 2014

@author: rodak
'''
import threading
from Queue import Queue, Empty
from time import sleep

import drmaa
from drmaa.errors import ExitTimeoutException, InvalidJobException
import math
from . import Settings

from Jobber import Executer, Logging

logger = Logging.logger("DRMAAJobExecuter", Settings.logDir+"/DRMAAJobExecuter.log")

maxNrOfJobs = Settings.drmaaMaxNrOfJobs

'''
An executer that will run jobs on a drmaa system
'''

class JobExecuter(Executer.Executer):

    def __init__(self, response):
        self.session = None
        self.nrOfRunning = 0
        Executer.Executer.__init__(self, response)
        self.jobQueue = []

    def onTerminate(self, executionId):
        self.session.control(str(executionId), drmaa.JobControlAction.TERMINATE)

    def onStatus(self, executionId):
        try:
            jobStatus = self.session.jobStatus(executionId)
        except InvalidJobException:
            jobStatus = "unknown"
        self.response.status(executionId, jobStatus)

    def onExecute(self, job, script, logDir):
        logger.info("Received message execute job "+str(job.jobId))
        if self.nrOfRunning < maxNrOfJobs:
            self._execJob(job, script, logDir)
        else:
            self.jobQueue.append((job, script, logDir))

    def _execJob(self, job, script, logDir):
        jobTemplate = self.transformJobToDRMAAJobTemplate(job, script, logDir)
        djobId = self.session.runJob(jobTemplate)
        logger.info("Executed job "+str(job.jobId)+" with execution id "+str(djobId))
        self.response.executionId(job.jobId, str(djobId))
        self.nrOfRunning += 1

    def _getJobError(self, val):
        if val.hasExited and val.exitStatus == 0:
            return None
        else:
            if val.hasExited:
                return "Failed because of exit value "+str(val.exitStatus)
            elif val.hasSignal:
                return "Failed because received signal "+str(val.terminatedSignal)
            elif val.wasAborted:
                return "Failed because was aborted"
            elif val.hasCoreDump:
                return "Failed because of core dump"
            else:
                return "Failed because of unknown error"

    def onRun(self):
        try:
            nr = 0
            while nr < 100:
                nr += 1
                retval = self.session.wait(drmaa.Session.JOB_IDS_SESSION_ANY, drmaa.Session.TIMEOUT_NO_WAIT)
                self.nrOfRunning -= 1
                while self.nrOfRunning < maxNrOfJobs and len(self.jobQueue) > 0:
                    mess = self.jobQueue.pop(0)
                    self._execJob(mess[0], mess[1], mess[2])
                logger.info("Job finished "+str(retval.jobId))
                self.response.finish(str(retval.jobId), self._getJobError(retval))
        except ExitTimeoutException:
            pass
        except InvalidJobException:
            pass
        except Exception, e:
            logger.warn(str(e))
            if e.message.startswith("code 24: no usage information was returned for the completed job"):
                pass
            else:
                logger.exception(str(e))

    def run(self):
        try:
            logger.info("started drmaa job executer")
            self.session = drmaa.Session()
            self.session.initialize()
            Executer.Executer.run(self)
        finally:
            self.session.exit()
            logger.info("drmaa job executer stopped")

    def transformJobToDRMAAJobTemplate(self, job, script, logDir):
        jt = self.session.createJobTemplate()
        nativeSpec = "-w n"
        nrOfCores = 1
        for opt in job.options:
            if opt.name == "cores":
                nrOfCores = opt.value
        for opt in job.options:
            if opt.name == "memory":
                val = opt.value
                memByCore = float(val[:-1]) / float(nrOfCores)
                memByCore = int(math.ceil(memByCore))
                nativeSpec += " -l membycore="+str(memByCore)+val[len(val) - 1]
            elif opt.name == "runtime":
                nativeSpec += " -l runtime="+opt.value
            elif opt.name == "cores":
                nativeSpec += " -pe smp "+opt.value
            elif not opt.name == 'module':
                nativeSpec += " -"+opt.name+" "+opt.value
        jt.nativeSpecification = nativeSpec
        jt.remoteCommand = script
        jt.outputPath = ":"+logDir+"/out"
        jt.errorPath = ":"+logDir+"/err"
        jt.jobName = job.name
        return jt