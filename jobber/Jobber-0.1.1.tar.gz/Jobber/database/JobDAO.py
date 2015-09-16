'''
Created on Jun 3, 2014

@author: rodak
'''
import os
import shutil
from Jobber import Settings
from Jobber.database import JobStatus, JobAction


class Option():
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Dependency():
    def __init__(self, dependency_id, dependency_status):
        self.dependencyId = dependency_id
        self.dependencyStatus = dependency_status
        
class NameAndParentName():
    def __init__(self, name, parentName = None):
        self.name = name
        self.parentName = parentName

    def equal(self, nameAndParentName):
        thisName = self
        otherName = nameAndParentName
        while thisName.name == otherName.name:
            if thisName.parentName is None:
                return otherName.parentName is None
            if otherName.parentName is None:
                return False
            thisName = thisName.parentName
            otherName = otherName.parentName
        return False


class PersistedJob():
    
    def __init__(self):
        self.dependencies = []

class JobDAO():
    
    def __init__(self, db):
        self.db = db

    def _booleanToYN(self, b):
        if b:
            return "Y"
        return "N"

    ################ Methods required by web interface  ###############################

    def getPipelines(self):
        self.db.execute("select * from t_jobs where parent_id is NULL order by id desc")
        return self.db.fetchall()

    def getMembers(self, JobID):
        self.db.execute("select * from t_jobs where parent_id = %i order by id" % JobID)
        return self.db.fetchall()

    def updateCommand(self, JobID, new_command):
        self.db.execute("update t_jobs set job_command=\"%s\" where id = %i;" % (new_command, JobID))

    ################ Methods required by web interface  ###############################

    def getActiveJobs(self):
        res = []
        self.db.execute("SELECT * FROM t_jobs WHERE status = 'IDLE' and is_group_job = 'N'")
        for row in self.db.fetchall():
            job = self._rowToJob(row)
            res.append(job)
        return res

    def sendLaunchJobMessage(self, jobId, responseId = None):
        self.db.execute("INSERT INTO t_job_messages (t_job_id, type, response_id) VALUES (%s, 'launch', %s)", [jobId, responseId])

    def sendDeleteJobMessage(self, jobId, responseId = None):
        self.db.execute("INSERT INTO t_job_messages (t_job_id, type, response_id) VALUES (%s, 'delete', %s)", [jobId, responseId])

    def sendChangeStatusJobMessage(self, jobId, status, recursive = False, response_id = None):
        self.db.execute("INSERT INTO t_job_messages (t_job_id, type, message, response_id) VALUES (%s, 'status', %s, %s)", [jobId, status+":"+str(recursive), response_id])

    def retreiveJobMessages(self, handlerId):
        self.db.execute("UPDATE t_job_messages SET transaction_id = %s WHERE transaction_id is null", [handlerId])
        self.db.execute("SELECT * FROM t_job_messages WHERE transaction_id = %s", [handlerId])
        return self.db.fetchall()

    def sendResponse(self, responseId, success, message):
        dbSuccess = 0
        if success:
            dbSuccess = 1
        self.db.execute("INSERT INTO t_job_responses (id, success, message) VALUES (%s, %s, %s)", [responseId, dbSuccess, message]);

    def removeMessageTransactionId(self, trId):
        self.db.execute("UPDATE t_job_messages SET transaction_id = NULL WHERE transaction_id = %s", [trId])

    def removeAllMessageTransactionIds(self):
        self.db.execute("UPDATE t_job_messages SET transaction_id = NULL")

    def deleteMessagesWithId(self, trId):
        self.db.execute("DELETE FROM t_job_messages WHERE transaction_id = %s", [trId])

    def getActiveJobIds(self):
        res = []
        self.db.execute("SELECT id FROM t_jobs WHERE status = 'IDLE' and is_group_job = 'N'")
        for row in self.db.fetchall():
            res.append(row['id'])
        return res

    def getRunningJobIds(self):
        res = []
        self.db.execute("SELECT id FROM t_jobs WHERE status = 'RUNNING' and is_group_job = 'N'")
        for row in self.db.fetchall():
            res.append(row['id'])
        return res

    def getJobWithDrmaaId(self, drmaaId):
        self.db.execute("SELECT * FROM t_jobs WHERE drmaa_id = %s", [drmaaId])
        res = self.db.fetchone()
        if res is not None:
            res = self._rowToJob(res)
        return res

    def setRunningJobsToIdle(self):
        self.db.execute("UPDATE t_jobs SET status = 'IDLE' WHERE status = 'RUNNING' and is_group_job = 'N'")

    def getTotalRuntime(self, jobId):
        time = 0
        if self.isGroupJob(jobId):
            for jid in self.getGroupMemebers(jobId):
                time += self.getTotalRuntime(jid)
        else:
            jobInfo = self.getJobInfo(jobId)
            time = (jobInfo['end_run_date'] - jobInfo['start_run_date']).total_seconds()
        return time

    def persistNewJob(self, job):
        self.db.execute("""INSERT INTO t_jobs(name, parent_id, description, status, job_command, is_unique,
            unique_key, is_group_job, max_parallel_nr, max_nr_of_restarts, current_run, delete_time, who_create, who_update, executer)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               [job.name, job.parentId, job.description, job.status, job.command, self._booleanToYN(job.unique), job.uniqueKey,
                                self._booleanToYN(job.groupJob), job.maxParallelNr, job.maxNrOfRestarts, job.currentRun, job.deleteTime,
                                job.whoCreate, job.whoUpdate, job.executer])
        job.jobId = self.db.insert_id()
        self.persistJobDependencies(job)
        self.persistJobOptions(job)
        return job.jobId

    def updateStartSubmitDate(self, jobId, date):
        self.db.execute("UPDATE t_jobs SET start_submit_date = %s WHERE id = %s", [date, jobId])

    def updateEndSubmitDate(self, jobId, date):
        self.db.execute("UPDATE t_jobs SET end_submit_date = %s WHERE id = %s", [date, jobId])

    def updateStartRunDate(self, jobId, date):
        self.db.execute("UPDATE t_jobs SET start_run_date = %s WHERE id = %s", [date, jobId])

    def updateEndRunDate(self, jobId, date):
        self.db.execute("UPDATE t_jobs SET end_run_date = %s WHERE id = %s", [date, jobId])

    def updateDRMAAId(self, jobId, drmaaId):
        self.db.execute("UPDATE t_jobs set drmaa_id = %s WHERE id = "+str(jobId), [drmaaId])

    def updateError(self, jobId, error):
        self.db.execute("UPDATE t_jobs set error = %s WHERE id = %s", [error, jobId])

    def deleteJob(self, jobId):
        if self.isGroupJob(jobId):
            members = self.getGroupMemebers(jobId)
            for member in members:
                self.deleteJob(member)
        else:
            logDir = Settings.logDir+"/"+str(jobId)
            if os.path.exists(logDir):
                shutil.rmtree(logDir)
        self.db.execute("DELETE FROM t_jobs WHERE id = %s", [jobId])
        self.db.execute("DELETE FROM t_job_dependencies WHERE t_job_id = %s", [jobId])
        self.db.execute("DELETE FROM t_job_options WHERE t_job_id = %s", [jobId])

    def getExistingUniqueJobId(self, job):
        if job.unique:
            uniqueKey = job.uniqueKey
            parentId = job.parentId
            args = []
            command = "SELECT * FROM t_jobs WHERE "
            if parentId is not None:
                command += "parent_id = %s AND "
                args.append(parentId)
            if uniqueKey is None:
                uniqueKey = job.command
                command += " job_command = %s"
            else:
                command += " unique_key = %s"
            args.append(uniqueKey)
            self.db.execute(command, args)
            job = self.db.fetchone()
            if job is None:
                return job
            return self._rowToJob(job)

    def getJobInfo(self, jobId):
        command = "SELECT * FROM t_jobs WHERE id = %s"
        self.db.execute(command, [jobId])
        return self.db.fetchone()

    def isRetryJob(self, jobId):
        job = self.getJobWithId(jobId)
        if job.currentRun < job.maxNrOfRestarts:
            return True
        return False

    def canActivateJob(self, jobId):
        jinfo = self.getJobInfo(jobId)
        if (('t_parent_id' not in jinfo) or jinfo['t_parent_id'] is None) and jinfo['max_parallel_nr'] > 0:
            self.db.execute("SELECT count(*) as c FROM t_jobs WHERE status = 'RUNNING' and name = '"+jinfo['name']+"'")
            running = self.db.fetchone()['c']
            return jinfo['max_parallel_nr'] > running
        else:
            return True

    def activateJob(self, jobId):
        if self.isGroupJob(jobId):
            for jid in self.getGroupMemebers(jobId):
                self.activateJob(jid)
        if self.getJobStatus(jobId) == JobStatus.DEACTIVATED:
            self.updateJobStatus(jobId, JobStatus.IDLE)

    def getActivableJob(self, name):
        self.db.execute("SELECT id, max_parallel_nr FROM t_jobs WHERE status = 'SUSPENDED' AND name= '"+name+"' ORDER BY id LIMIT 1")
        res = self.db.fetchone()
        if res is not None:
            return res['id']
        return None


    def persistJobDependencies(self, job):
        for dependency in job.dependencies:
            self.db.execute("""
                    INSERT INTO t_job_dependencies(t_job_id, t_job_dependency_id, dependency_job_status) VALUES (%s, %s, %s)
                """, [job.jobId, dependency.dependencyId, dependency.dependencyStatus])
    
    def persistJobOptions(self, job):
        for option in job.options:
            self.db.execute("""
                    INSERT INTO t_job_options (t_job_id, option_name, option_value) VALUES (%s, %s, %s)
                """, [job.jobId, option.name, option.value])

    def isGroupJob(self, jobId):
        self.db.execute("SELECT is_group_job FROM t_jobs WHERE id = %s", [jobId])
        gj = self.db.fetchone()['is_group_job']
        return gj == "Y"

    def getDependentJobs(self, jobId):
        self.db.execute("SELECT t_job_id FROM t_job_dependencies WHERE t_job_dependency_id = %s", [jobId])
        r = []
        for row in self.db.fetchall():
            r.append(row['t_job_id'])
        return r

    def getAffectedJobs(self, jobId):
        deps = self.getDependentJobs(jobId)
        res = []
        for dep in deps:
            if self.isGroupJob(dep):
                res += self.getNoneGroupMembersRecursive(dep)
            else:
                res.append(dep)
        return res

    def getParentId(self, jobId):
        self.db.execute("SELECT parent_id FROM t_jobs WHERE id = %s", [jobId])
        f = self.db.fetchone()
        if f is None:
            return f
        return f['parent_id']
        
    def updateJobStatus(self, jobId, status):
        self.db.execute("UPDATE t_jobs SET status = '"+status+"' WHERE id = "+str(jobId))

    def updateRun(self, jobId):
        self.db.execute("UPDATE t_jobs SET current_run = current_run + 1 WHERE id = "+str(jobId))
    
    def getJobWithId(self, jobId):
        self.db.execute("SELECT * FROM t_jobs WHERE id = "+str(jobId))
        for row in self.db.fetchall():
            return self._rowToJob(row)
        return None

    def getGroupMemebers(self, jobId):
        self.db.execute("SELECT id FROM t_jobs WHERE parent_id = "+str(jobId))
        res = []
        for row in self.db.fetchall():
            res.append(row['id'])
        return res

    def getNoneGroupMembers(self, jobId):
        self.db.execute("SELECT id FROM t_jobs WHERE parent_id = "+str(jobId)+" and is_group_job = 'N'")
        res = []
        for row in self.db.fetchall():
            res.append(row['id'])
        return res

    def getNoneGroupMembersRecursive(self, jobId):
        members = self.getGroupMemebers(jobId)
        res = []
        for jid in members:
            if self.isGroupJob(jid):
                res += self.getNoneGroupMembersRecursive(jid)
            else:
                res.append(jid)
        return res

    def isGroupJobFailed(self, groupJobId):
        self.db.execute("SELECT count(*) as c from t_jobs where parent_id = %s AND status = 'FAILED'", [groupJobId])
        return self.db.fetchone()['c'] > 0

    def isGroupJobCancelled(self, groupJobId):
        self.db.execute("SELECT count(*) as c from t_jobs where parent_id = %s AND status = 'CANCELLED'", [groupJobId])
        return self.db.fetchone()['c'] > 0

    def isGroupJobRunning(self, groupJobId):
        self.db.execute("SELECT count(*) as c from t_jobs where parent_id = %s AND status = 'RUNNING'", [groupJobId])
        return self.db.fetchone()['c'] > 0

    def isGroupJobFinished(self, groupJobId):
        self.db.execute("select count(*) as c from t_jobs where parent_id = %s", [groupJobId])
        total = self.db.fetchone()['c']
        self.db.execute("select count(*) as c from t_jobs where parent_id = %s and status = 'FINISHED'", [groupJobId])
        totalFinished = self.db.fetchone()['c']
        return total == totalFinished
    
    def getJobDependencyIds(self, jobId):
        self.db.execute("SELECT t_job_dependency_id, dependency_job_status FROM t_job_dependencies WHERE t_job_id = "+str(jobId))
        res = []
        for row in self.db.fetchall():
            res.append(Dependency(row['t_job_dependency_id'], row['dependency_job_status']))
        return res

    def getParentJobDependencyIds(self, jobId):
        parentId = self.getParentId(jobId)
        if parentId is None:
            return []
        res = self.getJobDependencyIds(parentId)
        return res + self.getParentJobDependencyIds(parentId)

    def getJobStatus(self, jobId):
        self.db.execute("SELECT status FROM t_jobs WHERE id = (%s)", [jobId])
        return self.db.fetchone()['status']

    def getGroupJobAction(self, jobId):
        jobStatus = self.getJobStatus(jobId)
        if self.isGroupJobFailed(jobId):
            return JobAction.NOTHING if jobStatus == JobStatus.FAILED else JobAction.FAIL
        if self.isGroupJobCancelled(jobId):
            return JobAction.CANCEL if jobStatus != JobStatus.CANCELLED else JobAction.NOTHING
        if self.isGroupJobFinished(jobId):
            return JobAction.FINISH_GROUP if jobStatus != JobStatus.FINISHED else JobAction.NOTHING
        if self.isGroupJobRunning(jobId):
            return JobAction.EXECUTE if jobStatus != JobStatus.RUNNING else JobAction.NOTHING
        else:
            return JobAction.IDLE_GROUP if jobStatus != JobStatus.IDLE else JobAction.NOTHING

    def getNameWithParentNames(self, jobId):
        jobInfo = self.getJobInfo(jobId)
        name = jobInfo['name']
        parent = jobInfo['parent_id']
        parentName = None
        if parent is not None:
            parentName = self.getNameWithParentNames(parent)
        return NameAndParentName(name, parentName)

    def getIdleMaxParallelRunningJobsWithParentAndParentNames(self, nameAndParentNames):
        name = nameAndParentNames.name
        self.db.execute("SELECT id FROM t_jobs WHERE status = 'IDLE' AND name = %s and max_parallel_nr > 0", [name])
        res = []
        for row in self.db.fetchall():
            jobId = row['id']
            npn = self.getNameWithParentNames(jobId)
            if npn.equal(nameAndParentNames):
                res.append(jobId)
        return res

    def getRunningJobsWithNameAndParentNames(self, nameAndParentNames):
        name = nameAndParentNames.name
        self.db.execute("SELECT id FROM t_jobs WHERE status = 'RUNNING' AND name = %s", [name])
        res = []
        for row in self.db.fetchall():
            jobId = row['id']
            npn = self.getNameWithParentNames(jobId)
            if npn.equal(nameAndParentNames):
                res.append(jobId)
        return res

    def getMaxNrOfRunning(self, jobId):
        self.db.execute("SELECT max_parallel_nr FROM t_jobs WHERE id = %s", [jobId])
        row = self.db.fetchone()
        running = row['max_parallel_nr']
        return running

    def getJobAction(self, jobId):
        jobStatus =  self.getJobStatus(jobId)
        if jobStatus != JobStatus.IDLE and jobStatus != JobStatus.RUNNING:
            return JobAction.NOTHING
        deps = self.getJobDependencyIds(jobId) + self.getParentJobDependencyIds(jobId)
        res = JobAction.EXECUTE
        for dep in deps:
            depStat = dep.dependencyStatus
            stat = self.getJobStatus(dep.dependencyId)
            if depStat != stat:
                return JobAction.NOTHING
        if res == JobAction.EXECUTE:
            if jobStatus != JobStatus.IDLE:
                return JobAction.NOTHING
        return res

    def getJobIdsWithFinishedDirectDependencies(self):
        self.db.execute("c")

    def getFailureReason(self):
        return self.failReason

    def getOptions(self, jobId):
        parentJobId = self.getParentId(jobId)
        parentOptions = []
        if parentJobId is not None:
            parentOptions = self.getOptions(parentJobId)
        self.db.execute("SELECT option_name, option_value FROM t_job_options WHERE t_job_id = "+str(jobId))
        res = []
        for pOpt in parentOptions:
            res.append(pOpt)
        for row in self.db.fetchall():
            res.append(Option(row['option_name'], row['option_value']))
        return res

    def getExecuter(self, jobId):
        self.db.execute("SELECT executer FROM t_jobs WHERE id = "+str(jobId))
        row = self.db.fetchone()
        if row is None:
            return Settings.defaultExecuter
        else:
            if row['executer'] is not None:
                return row['executer']
            else:
                parent = self.getParentId(jobId)
                if parent is not None:
                    return self.getExecuter(parent)
                return Settings.defaultExecuter


    def _rowToJob(self, row):
        job = PersistedJob()
        job.jobId = row['id']
        isGroup = row['is_group_job']
        if 'name' in row:
            job.name = row['name']
        else:
            job.name = None
        if 'description' in row:
            job.description = row['description']
        else:
            job.description = None
        job.status = row['status']
        job.unique = row['is_unique'] == 'Y'
        if 'unique_key' in row:
            job.uniqueKey = row['unique_key']
        else:
            job.uniqueKey = None
        if 'startDate' in row:
            job.startDate = row['start_date']
        else:
            job.startDate = None
        if 'endDate' in row:
            job.endDate = row['end_date']
        else:
            job.endDate = None
        if 'delete_time' in row:
            job.deleteTime = row['delete_time']
        else:
            job.deleteTime = None
        if 'who_create' in row:
            job.whoCreate = row['who_create']
        else:
            job.whoCreate = None
        if 'who_update' in row:
            job.whoUpdate = row['who_update']
        else:
            job.whoUpdate = None
        if 'parent_id' in row:
            job.parentId = row['parent_id'];
        else:
            job.parentId = None
        job.maxParallelNr = row['max_parallel_nr']
        job.maxNrOfRestarts = row['max_nr_of_restarts']
        job.currentRun = row['current_run']
        job.executer = self.getExecuter(job.jobId)
        job.dependencies = self.getJobDependencyIds(job.jobId)
        job.options = self.getOptions(job.jobId)
        if isGroup == 'Y':
            job.groupJob = True
            job.command = None
            job.drmaaId = None
        else:
            job.groupJob = False

            if 'drmaa_id' in row:
                job.drmaaId = row['drmaa_id']
            else:
                job.drmaaId = None
            job.command = row['job_command']
        return job
        
