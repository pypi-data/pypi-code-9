import uuid

from Jobber import Executer


__author__ = 'rodak'

'''
A simple executer that just reports a job as successfully executed without executing it. For testing purposes.
'''

class JobExecuter(Executer.Executer):

    def __init__(self, response):
        Executer.Executer.__init__(response)

    def onExecute(self, job, script, logDir):
        exId = str(uuid.uuid4())
        self.response.executionId(job.jobId, exId)
        self.response.finish(exId, None)

    def onStatus(self, executionId):
        self.response.status(executionId, "unknown")

    def onTerminate(self, executionId):
        pass