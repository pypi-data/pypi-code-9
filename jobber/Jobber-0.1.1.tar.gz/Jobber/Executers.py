import Queue
from Queue import Empty
import os
from Jobber import Logging, Settings, JobExecuter

'''
Usage:

executer = Executers.create(messageHandler)
executer.run(job)

where:
    messageHandler an object of type MessageHandler
    job is a database job. see class "JobCreator" in module "database".

'''


__author__ = 'rodak'
executers = {}

if "JOBBER_EXECUTERS" in os.environ:
    execfile(os.environ["JOBBER_EXECUTERS"])
else:
    execfile(os.path.join(os.path.expanduser("~"), ".jobber")+"/executers.py")

logger = Logging.logger("Executers", Settings.logDir+"/Executers.log")

def _createExecuters(listener):
    idToExecuter = {};
    for name in executers.keys():
        executer = executers[name]
        idToExecuter[name] = executer(listener)
        idToExecuter[name].start()
        logger.info("Loaded executer "+name)
    return idToExecuter


class ResponseHandler():

    def __init__(self):
        self.queue = Queue.Queue()
        self.batchNr = 100

    def _addMessage(self, message):
        self.queue.put(message)

    def executionId(self, jobId, executerId):
        self.queue.put(("execution", jobId, executerId))

    def finish(self, executerId, error = None):
        self.queue.put(("finish", executerId, error))

    def status(self, executionId, jobStatus):
        self.queue.put(("status", executionId, jobStatus))

    def onExecutionId(self, jobId, executerId):
        raise Exception("onUpdateId must be implemented by subclasses")

    def onFinish(self, executerId, error):
        raise Exception("onJobFinished must be implemented by subclasses")

    def onStatus(self, jobId, status):
        pass

    def handleMessages(self):
        try:
            nr = 0
            while nr < self.batchNr:
                nr += 1
                mess = self.queue.get(False)
                if mess[0] == "execution":
                    self.onExecutionId(mess[1], mess[2])
                elif mess[0] == "finish":
                    self.onJobFinished(mess[1], mess[2])
                elif mess[0] == "status":
                    self.onStatus(mess[1], mess[2])
        except Empty:
            pass

class MultiExecuter():

    def __init__(self, messageHandler):
        self.idToExecuter = _createExecuters(messageHandler)
        self.messageHandler = messageHandler

    def run(self, job):
        logger.info("executing job "+str(job.jobId))
        logDir = JobExecuter.createLogDir(job)
        script = JobExecuter.createRunScript(job)
        ex = job.executer
        if job.executer not in self.idToExecuter:
            logger.warn("Executer with id "+ex+" does not exist for job with id "+str(job.jobId)+", falling back to executer "+Settings.defaultExecuter)
            ex = Settings.defaultExecuter
        self.idToExecuter[ex].execute(job, script, logDir)

    def handleMessages(self):
        self.messageHandler.handleMessages()

    def terminate(self, executer, executionId):
        if executer not in self.idToExecuter:
            logger.warn("Executer with id "+executer+" does not exist for job with id "+str(job.jobId)+", falling back to executer "+Settings.defaultExecuter)
            executer = Settings.defaultExecuter
        self.idToExecuter[executer].terminate(executionId)



    def stop(self):
        for ex in self.idToExecuter:
            self.idToExecuter[ex].stop()

def create(handler):
    return MultiExecuter(handler)
