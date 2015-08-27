'''
Created on Jun 5, 2014

@author: rodak
'''
import threading
from Queue import Queue, Empty
from time import sleep
from . import Native
from .JobExecuter import DRMAAResponse, JOB_FINISHED

EXECUTE_JOB = "Execute"
TERMINATE_JOB = "Terminate"
JOB_STATUS = "Status"
STOP = "stop"

class JobMessage():

    def __init__(self, messType, message):
        self.type = messType
        self.message = message

class RunJob():

    def __init__(self, job, listener):
        self.jobAndScript = job
        self.listener = listener

class DRMAARetVal():
    pass

class DRMAAJobActor(threading.Thread):
    
    def __init__(self, results):
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.results = results
        self.running = True
        self.pooledExecuter = Native.SystemCommandPooledExecuter()

    def terminateJob(self, jobId):
        self.queue.put(JobMessage(TERMINATE_JOB, jobId))

    def runJob(self, job, listener):
        self.queue.put(JobMessage(EXECUTE_JOB, RunJob(job, listener)))

    def stop(self):
        self.running = False
        self.pooledExecuter.stop()
        self.queue.put(JobMessage(STOP, None))

    def start(self):
        super(DRMAAJobActor, self).start()
        self.pooledExecuter.start()

    def processCommandResult(self, result):
        retval = DRMAARetVal()
        if result.status == Native.TIMEOUT or result.status == Native.KILLED:
            result.wasAborted = True
        else:
            retval.hasExited = True
            retval.exitStatus = result.returnCode
        retval.jobId = result.jobId
        self.results(DRMAAResponse(JOB_FINISHED, retval))


    def run(self):
        try:
            while self.running:
                wait = True
                try:
                    mess = self.queue.get(False)
                    wait = False
                    if mess.type == EXECUTE_JOB:
                        jobAndScript = mess.message.jobAndScript
                        runJobMess = Native.RunJobMessage(jobAndScript.script, jobAndScript.logDir+"/out", jobAndScript.logDir+"/err", lambda res: self.processCommandResult(res))
                        runJobMess.maxRuntime = 60*60*24
                        lastId = self.pooledExecuter.execute(runJobMess)
                        mess.message.listener(lastId)
                    elif mess.type == JOB_STATUS:
                        jobId = mess.message
                        jobStatus = "unknown"
                        mess.message.listener(jobStatus)
                    elif mess.type == TERMINATE_JOB:
                        jobId = mess.message
                        self.pooledExecuter.kill(jobId)
                    elif mess.type == STOP:
                        self.running = False
                        break
                except Empty:
                    pass
                if wait:
                    sleep(0.2)
        finally:
            pass
