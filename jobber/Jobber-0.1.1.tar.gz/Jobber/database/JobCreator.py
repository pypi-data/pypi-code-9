from Jobber.database import JobStatus


class Job():
    def __init__(self):
        pass

class JobCreator():

    def __init__(self):
        self.outputPath = None
        self.reset()


    def reset(self):
        self.maxNrOfParallelJobs = 0
        self.maxNrOfRestarts = 3
        self.name = "anonymous"
        self.description = "none"
        self.uniqueJob = False
        self.uniqueKey = None
        self.groupJob = False
        self.dependencies = []
        self.options = []
        self.members = []
        self.deleteTime = 0
        self.executer = None

    def createJob(self, command):
        job = Job()
        job.name = self.name
        job.description = self.description
        job.status = JobStatus.DEACTIVATED
        job.command = command
        job.unique = self.uniqueJob
        job.uniqueKey = self.uniqueKey
        job.groupJob = self.groupJob
        job.startDate = None
        job.endDate = None
        job.maxParallelNr = self.maxNrOfParallelJobs
        job.maxNrOfRestarts = self.maxNrOfRestarts
        job.currentRun = 0
        job.deleteTime = self.deleteTime
        job.whoCreate = None
        job.whoUpdate = None
        job.options = self.options
        job.dependencies = self.dependencies
        job.members = self.members
        job.parentId = None
        job.executer = self.executer
        self.reset()
        return job