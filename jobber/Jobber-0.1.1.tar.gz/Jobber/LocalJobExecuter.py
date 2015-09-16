'''
Created on Jun 5, 2014

@author: rodak
'''
from . import Native

from . import Executer
from . import Logging
from Jobber import Settings

logger = Logging.logger("LocalJobExecuter", Settings.logDir+"/LocalJobExecuter.log")

'''
An executer that will run jobs locally
'''

class JobExecuter(Executer.Executer):

    def __init__(self, response):
        Executer.Executer.__init__(self, response)
        self.pooledExecuter = Native.SystemCommandPooledExecuter()

    def start(self):
        Executer.Executer.start(self)
        self.pooledExecuter.start()
        logger.info("LocalJobExecuter Started")

    def onStop(self):
        self.pooledExecuter.stop()
        logger.info("LocalJobExecuter Stopped")

    def onExecute(self, job, script, logDir):
        logger.info("Execute job "+str(job.jobId))
        runJobMess = Native.RunJobMessage(script, logDir+"/out", logDir+"/err", lambda res: self.processCommandResult(res))
        runJobMess.maxRuntime = 60*60*24
        lastId = self.pooledExecuter.execute(runJobMess)
        self.response.executionId(job.jobId, lastId)

    def processCommandResult(self, result):
        error = None
        if result.status == Native.TIMEOUT:
            error = "Job timed out"
        elif result.status == Native.KILLED:
            error = "Job was killed"
        else:
            if result.returnCode != 0:
                error = "Job exited with exit status "+str(result.returnCode)
        self.response.finish(result.jobId, error)

    def onTerminate(self, executionId):
        logger.info("Kill execution "+executionId)
        self.pooledExecuter.kill(executionId)

    def onStatus(self, executionId):
        self.response.status(executionId, "unknown")