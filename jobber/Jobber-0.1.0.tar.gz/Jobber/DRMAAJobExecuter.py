'''
Created on Jun 5, 2014

@author: rodak
'''
import logging
import re
import threading
from Queue import Queue, Empty
from time import sleep

import drmaa
from drmaa.errors import ExitTimeoutException, InvalidJobException
import math
from . import Settings

from .JobExecuter import DRMAAResponse, JOB_FINISHED
logger = logging.getLogger("DRMAAJobExecuter")
handler = logging.FileHandler(Settings.logDir+"/DRMAAJobExecuter.log")
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(handler)

EXECUTE_JOB = "Execute"
TERMINATE_JOB = "Terminate"
JOB_STATUS = "Status"
STOP = "stop"

maxNrOfJobs = Settings.drmaaMaxNrOfJobs

class DRMAAMessage():

    def __init__(self, messType, message):
        self.type = messType
        self.message = message


class RunJob():

    def __init__(self, job, listener):
        self.jobAndScript = job
        self.listener = listener

class DRMAAJobActor(threading.Thread):
    
    def __init__(self, results):
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.results = results
        self.running = True

    def terminateJob(self, jobId):
        self.queue.put(DRMAAMessage(TERMINATE_JOB, jobId))

    def runJob(self, job, listener):
        self.queue.put(DRMAAMessage(EXECUTE_JOB, RunJob(job, listener)))

    def transformJobToDRMAAJobTemplate(self, jobAndScript):
        job = jobAndScript.job
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
        logDir = jobAndScript.logDir
        jt.remoteCommand = jobAndScript.script
        jt.outputPath = ":"+logDir+"/out"
        jt.errorPath = ":"+logDir+"/err"
        jt.jobName = job.name
        return jt

    def stop(self):
        self.running = False
        self.queue.put(DRMAAMessage(STOP, None))

    def run(self):
        try:
            logger.info("started drmaa job executer")
            self.session = drmaa.Session()
            self.session.initialize()
            queue = []
            nrOfRunning = 0
            while self.running:
                wait = True
                try:
                    mess = self.queue.get(False)
                    wait = False
                    if mess.type == EXECUTE_JOB:
                        logger.info("Received message execute job "+str(mess.message.jobAndScript.job.jobId))
                        if nrOfRunning < maxNrOfJobs:
                            jobScript = mess.message.jobAndScript
                            jobTemplate = self.transformJobToDRMAAJobTemplate(jobScript)
                            djobId = self.session.runJob(jobTemplate)
                            logger.info("Executed job "+str(mess.message.jobAndScript.job.jobId)+" with execution id "+str(djobId))
                            mess.message.listener(djobId)
                            nrOfRunning += 1
                        else:
                            queue.append(mess)
                    elif mess.type == JOB_STATUS:
                        jobId = mess.message.jobId
                        try:
                            jobStatus = self.session.jobStatus(jobId)
                        except InvalidJobException:
                            jobStatus = "unknown"
                        mess.message.listener(jobStatus)
                    elif mess.type == TERMINATE_JOB:
                        self.session.control(str(mess.message), drmaa.JobControlAction.TERMINATE)
                    elif mess.type == STOP:
                        self.running = False
                        break
                except Empty:
                    pass
                except InvalidJobException:
                    pass
                try:
                    retval = self.session.wait(drmaa.Session.JOB_IDS_SESSION_ANY, drmaa.Session.TIMEOUT_NO_WAIT)
                    wait = False
                    nrOfRunning -= 1
                    while nrOfRunning < maxNrOfJobs and len(queue) > 0:
                        mess = queue.pop(0)
                        jobScript = mess.message.jobAndScript
                        jobTemplate = self.transformJobToDRMAAJobTemplate(jobScript)
                        djobId = self.session.runJob(jobTemplate)
                        logger.info("Executed job "+str(jobScript.job.jobId)+" with execution id "+str(djobId))
                        mess.message.listener(djobId)
                        nrOfRunning += 1
                    logger.info("Job finished "+str(retval.jobId))
                    self.results(DRMAAResponse(JOB_FINISHED, retval))
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
                if wait:
                    sleep(0.2)
        finally:
            self.session.exit()
            logger.info("drmaa job executer stopped")
