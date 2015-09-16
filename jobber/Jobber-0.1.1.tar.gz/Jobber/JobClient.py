from . import database

__author__ = 'rodak'

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

class Jobber():

    def __init__(self):
        self.jobDAO = database.dao(database.getDB())
        self.parentIds = []
        self.jobCreator = database.JobCreator()
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
                    self.jobCreator.dependencies.append(database.JobDependency(long(jobId), stat))
            elif set == "options":
                for opt in settings[set]:
                    self.jobCreator.options.append(database.JobOption(opt[0], opt[1]))
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
        database.releaseDB(self.jobDAO.db)

JobberBuilder = Jobber
