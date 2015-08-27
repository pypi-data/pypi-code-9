from . import JobDAO
from . import Connection
from . import Settings

__author__ = 'rodak'

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

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
        job = JobDAO.Job()
        job.name = self.name
        job.description = self.description
        job.status = JobDAO.DEACTIVATED
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

class Jobber():

    def __init__(self):
        self.jobDAO = JobDAO.JobDAO(Connection.createDB())
        self.parentIds = []
        self.jobCreator = JobCreator()
        self.ignoreJobId = None

    def _setSettings(self, settings):
        for set in settings:
            if set == "name":
                self.jobCreator.name = settings[set]
            elif set == "dependencies":
                for dep in settings[set]:
                    stat = "FINISHED"
                    if not is_sequence(dep):
                        jobId = dep
                    else:
                        jobId = dep[0]
                        if len(dep) > 1:
                            stat = dep[1]
                    self.jobCreator.dependencies.append(JobDAO.Dependency(long(jobId), stat))
            elif set == "options":
                for opt in settings[set]:
                    self.jobCreator.options.append(JobDAO.Option(opt[0], opt[1]))
            elif set == "description":
                self.jobCreator.description = settings[set]
            elif set == "name":
                self.jobCreator.name = settings[set]
            elif set == "executer":
                self.jobCreator.executer = settings[set]
            elif set == "maxNrOfJobs":
                self.jobCreator.maxNrOfParallelJobs = int(settings[set])
            elif set == "uniqueId":
                self.jobCreator.uniqueJob = True
                uId = settings[set]
                if isinstance(uId, basestring):
                    self.jobCreator.uniqueKey = uId

    def job(self, command, settings = {}):
        if self.ignoreJobId is not None:
            return -1
        self._setSettings(settings)
        job = self.jobCreator.createJob(command)
        if len(self.parentIds) > 0:
            job.parentId = self.parentIds[len(self.parentIds) - 1]
        existingJob = self.jobDAO.getExistingUniqueJobId(job)
        if existingJob is not None:
            return existingJob.jobId
        else:
            newJob = self.jobDAO.persistNewJob(job)
            return newJob

    def startGroup(self, settings = {}):
        if self.ignoreJobId is not None:
            self.parentIds.append(-1)
            return -1
        self._setSettings(settings)
        self.jobCreator.groupJob = True
        job = self.jobCreator.createJob("GROUP")
        if len(self.parentIds) > 0:
            job.parentId = self.parentIds[len(self.parentIds) - 1]
        existingJob = self.jobDAO.getExistingUniqueJobId(job)
        if existingJob is not None:
            self.ignoreJobId =  existingJob.jobId
            self.parentIds.append( existingJob.jobId)
            return  existingJob.jobId
        else:
            newJob = self.jobDAO.persistNewJob(job)
            self.parentIds.append(newJob)
            return newJob

    def extendGroup(self, groupId):
        self.parentIds.append(groupId)

    def endGroup(self):
        jobId = self.parentIds.pop()
        if self.ignoreJobId is not None:
            if self.ignoreJobId == jobId:
                self.ignoreJobId = None

    def launch(self, jobId):
        self.jobDAO.sendLaunchJobMessage(jobId)

    def delete(self, jobId):
        self.jobDAO.sendDeleteJobMessage(jobId)

    def changeStatus(self, jobId, status, recursive = False, resonse_id = None):
        self.jobDAO.sendChangeStatusJobMessage(jobId, status, recursive, resonse_id)

    def close(self):
        self.jobDAO.db.close()

JobberBuilder = Jobber
