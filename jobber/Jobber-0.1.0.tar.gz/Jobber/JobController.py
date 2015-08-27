'''
Created on May 12, 2014

@author: rodak
'''
import logging

from subprocess import Popen
import threading
from Queue import Queue
import datetime
import traceback
from uuid import uuid4
import time
import os

from . import Connection
from . import JobDAO, JobExecuter, Executers, Settings

loggerJobController = logging.getLogger("JobController")
handler = logging.FileHandler(Settings.logDir+"/JobController.log")
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
loggerJobController.addHandler(handler)
loggerMessageHandler = logging.getLogger("Message handler")
handler = logging.FileHandler(Settings.logDir+"/MessageHandler.log")
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
loggerMessageHandler.addHandler(handler)


class BashJob():

    def __init__(self, output):
        self.script = output+"/command.sh"
        self.out = open(output+"/out", "w")
        self.err = open(output+"/err", "w")
        self.process = Popen([self.script], stdout=self.out, stderr=self.err, shell=True)

    def poll(self):
        return self.process.poll()

    def kill(self):
        self.process.kill()

class JobStatusUpdateEvent():

    def __init__(self, id, status):
        self.id = id
        self.status = status

DRMAA_ID_UPDATE = "DrmaaIdUpdate"

class UpdateDRMAAIdMessage():

    def __init__(self, job, drmaaId):
        self.job = job
        self.drmaaId = drmaaId


DRMAA_INFO = 1
START_JOB = 2
ACTIVATE_JOB = 3
SET_JOB_STATUS = 4
REMOVE_DELETED_JOBS = 5
DELETE_OUTDATED_JOBS = 6
DELETE_JOB = 7
STOP=8

TRIGGER = 1
NOTHING = 2
FAILED_TRIGGER = 3

def createJobDAO():
    return JobDAO.JobDAO(Connection.createDB())

class JobManagerProcess(threading.Thread):

    def registerForUpdates(self, job):
        self.updateableJobs.append(job)

    def getOrCreateJobDAO(self):
        if self.jobDAO is None:
            self.jobDAO = createJobDAO()
        return self.jobDAO

    def closeJobDAO(self):
        self.jobDAO.db.close()
        self.jobDAO = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.processing = False
        self.daemon = True
        self.queue = Queue()
        self.groups = set()
        self.jobDAO = None
        self.idToExecuter = {}
        self.running = True
        self.idToExecuter.keys()
        for name in Executers.executers.keys():
            executer = Executers.executers[name]
            self.idToExecuter[name] = executer(lambda mess: self.queue.put([DRMAA_INFO, mess]))
            self.idToExecuter[name].start()
            loggerJobController.info("Loaded executer "+name)

    def processActiveJobs(self):
        if self.processing:
            return
        self.processing = True
        while (len(self.jobs) > 0) or (len(self.groups) > 0):
            active = sorted(self.jobs)
            self.jobs = set([])
            for jobId in active:
                self.chooseAction(jobId)
                parent = self.jobDAO.getParentId(jobId)
                if parent is not None:
                    self.groups.add(parent)
                else:
                    name = self.jobDAO.getJobInfo(jobId)['name']
                    activable = self.jobDAO.getActivableJob(name)
                    if activable is not None:
                        self.launchJob(activable)
            newGroups = set([])
            for gid in self.groups:
                action = self.jobDAO.getGroupJobAction(gid)
                if action == JobDAO.CANCEL:
                    self.jobDAO.updateJobStatus(gid, JobDAO.CANCELLED)
                elif action == JobDAO.FAIL:
                    self.jobDAO.updateJobStatus(gid, JobDAO.FAILED)
                elif action == JobDAO.FINISH_GROUP:
                    self.jobDAO.updateJobStatus(gid, JobDAO.FINISHED)
                    for jid in self.jobDAO.getAffectedJobs(gid):
                        self.jobs.add(jid)
                elif action == JobDAO.EXECUTE:
                    self.jobDAO.updateJobStatus(gid, JobDAO.RUNNING)
                elif action == JobDAO.IDLE_GROUP:
                    self.jobDAO.updateJobStatus(gid, JobDAO.IDLE)
                if action != JobDAO.NOTHING:
                    parent = self.jobDAO.getParentId(gid)
                    if parent is not None:
                        newGroups.add(parent)
                    else:
                        name = self.jobDAO.getJobInfo(gid)['name']
                        activable = self.jobDAO.getActivableJob(name)
                        if activable is not None:
                            self.launchJob(activable)
            self.groups = newGroups
        self.processing = False

    def stop(self):
        self.running = False
        self.queue.put([STOP])
        for ex in self.idToExecuter.values():
            ex.stop()

    def addAffectedJobs(self, jobId):
        for id in self.jobDAO.getAffectedJobs(jobId):
            self.jobs.add(id)
        parent = self.jobDAO.getParentId(jobId)
        if parent is not None:
            self.groups.add(parent)

    def chooseAction(self, jobId):
        action = self.jobDAO.getJobAction(jobId)
        if action == JobDAO.EXECUTE:
            loggerJobController.info("executing job "+str(jobId))
            self.jobDAO.updateJobStatus(jobId, JobDAO.RUNNING)
            self.jobDAO.updateRun(jobId)
            job = self.jobDAO.getJobWithId(jobId)
            self.jobDAO.updateStartSubmitDate(jobId, datetime.datetime.now())
            logDir = JobExecuter.createLogDir(job)
            script = JobExecuter.createRunScript(job)
            ex = job.executer
            if not job.executer in self.idToExecuter:
                loggerJobController.warn("Executer with id "+ex+" does not exist for job with id "+str(jobId)+", falling back to executer "+Settings.defaultExecuter)
                ex = Settings.defaultExecuter
            self.idToExecuter[ex].runJob(JobExecuter.JobAndScript(job, script, logDir), lambda drmaaId: self.sendMessage([DRMAA_INFO, JobExecuter.DRMAAResponse(DRMAA_ID_UPDATE, UpdateDRMAAIdMessage(jobId, drmaaId))]))

    def receiveDRMAAMessage(self, mess):
        type = mess.type
        val = mess.message
        if type == JobExecuter.JOB_FINISHED:
            drmaaId = val.jobId
            job = self.jobDAO.getJobWithDrmaaId(drmaaId)
            loggerJobController.info("Job with execution id "+str(drmaaId)+" finished")
            if job is not None and job.status != JobDAO.CANCELLED:
                jobId = job.jobId
                loggerJobController.info("Job with id "+str(jobId)+" finished")
                status = JobDAO.FAILED
                self.jobDAO.updateEndSubmitDate(jobId, datetime.datetime.now())
                startEnd = JobExecuter.readStartEndRun(job)
                if startEnd is not None:
                    self.jobDAO.updateStartRunDate(jobId, datetime.datetime.fromtimestamp(startEnd['start']))
                    self.jobDAO.updateEndRunDate(jobId, datetime.datetime.fromtimestamp(startEnd['end']))
                if val.hasExited and val.exitStatus == 0:
                    status = JobDAO.FINISHED
                    self.jobDAO.updateError(jobId, "")
                else:
                    if val.hasExited:
                        self.jobDAO.updateError(jobId, "Failed because of exit value "+str(val.exitStatus))
                    elif val.hasSignal:
                        self.jobDAO.updateError(jobId, "Failed because received signal"+str(val.terminatedSignal))
                    elif val.wasAborted:
                        self.jobDAO.updateError(jobId, "Failed because was aborted")
                    elif val.hasCoreDump:
                        self.jobDAO.updateError(jobId, "Failed because of core dump")
                    else:
                        self.jobDAO.updateError(jobId,
                        "Failed because of unknown error")
                if status == JobDAO.FAILED:
                    if self.jobDAO.isRetryJob(jobId):
                        self.jobDAO.updateJobStatus(jobId, JobDAO.IDLE)
                        self.jobs.add(jobId)
                        self.processActiveJobs()
                        return
                self.jobDAO.updateJobStatus(jobId, status)
                self.addAffectedJobs(jobId)
                self.processActiveJobs()
                if job.parentId is None:
                    activable = self.jobDAO.getActivableJob(job.name)
                    if activable is not None:
                        self.launchJob(activable)
            else:
                if job is None:
                    loggerJobController.warn("Job with execution id "+str(drmaaId)+" not found")
        if type == DRMAA_ID_UPDATE:
            loggerJobController.info("Job with id "+str(val.job)+" assigned execution id "+str(val.drmaaId))
            self.jobDAO.updateDRMAAId(val.job, val.drmaaId)

    def sendMessage(self, mess):
        self.queue.put(mess)

    def launchJob(self, jobId):
        if self.jobDAO.getJobWithId(jobId) is None:
            loggerJobController.warn("job "+str(jobId)+" cannot be launched because it doesn't exist")
            return
        status = self.jobDAO.getJobStatus(jobId)
        if status != JobDAO.DEACTIVATED or self.jobDAO.canActivateJob(jobId):
            loggerJobController.info("activating job "+str(jobId))
            self.jobDAO.activateJob(jobId)
            if self.jobDAO.isGroupJob(jobId):
                for jid in self.jobDAO.getNoneGroupMembersRecursive(jobId):
                    self.jobs.add(jid)
            else:
                self.jobs.add(jobId)
            self.processActiveJobs()

    def updateJobStatus(self, jobId, status, recursive, groupMembers):
        affectedJobs = set()
        job = self.jobDAO.getJobWithId(jobId)
        if not job.groupJob:
            affectedJobs.add(jobId)
        if job.status != status:
            if job.groupJob and (status != JobDAO.FINISHED or job.status != JobDAO.RUNNING) and groupMembers:
                for mId in self.jobDAO.getGroupMemebers(jobId):
                    affectedJobs.add(mId)
                    self.updateJobStatus(mId, status, recursive, groupMembers)
            if status == JobDAO.IDLE or status == JobDAO.CANCELLED:
                if not job.groupJob and job.status == JobDAO.RUNNING:
                    self.idToExecuter[job.executer].terminateJob(job.drmaaId)
                    self.jobDAO.updateDRMAAId(jobId, None)
                self.jobDAO.updateJobStatus(jobId, status)
            elif status == JobDAO.FINISHED:
                if job.status != JobDAO.RUNNING:
                    self.jobDAO.updateJobStatus(jobId, status)
        if recursive:
            depJobIds = self.jobDAO.getDependentJobs(jobId)
            for depId in depJobIds:
                for affId in self.updateJobStatus(depId, status, recursive, True):
                    affectedJobs.add(affId)
        return affectedJobs

    def respond(self, response_id, message):
        self.jobDAO.sendResponse(response_id, message);

    def run(self):
        loggerJobController.info("started job manager")
        self.getOrCreateJobDAO()
        running = self.jobDAO.getRunningJobIds()
        self.jobDAO.setRunningJobsToIdle()
        for id in running:
            j = self.jobDAO.getJobWithId(id)
            if j.drmaaId is not None:
                self.idToExecuter[j.executer].terminateJob(j.drmaaId)
                self.jobDAO.updateDRMAAId(id, None)
        self.jobs = set(self.jobDAO.getActiveJobIds())
        self.processActiveJobs()
        self.closeJobDAO()
        while self.running:
            try:
                req = self.queue.get()
                self.getOrCreateJobDAO()
                messageType = req[0]
                if messageType == START_JOB:
                    try:
                        jobId = req[1]
                        loggerJobController.info("Received message start job "+str(jobId))
                        self.launchJob(jobId)
                        if req[2] is not None:
                            self.jobDAO.sendResponse(req[2], True, "ok")
                    except Exception, e:
                        loggerJobController.exception(str(e))
                        if req[2] is not None:
                            self.jobDAO.sendResponse(req[2], False, e.message)
                        raise e
                elif messageType == DRMAA_INFO:
                    self.receiveDRMAAMessage(req[1])
                elif messageType == SET_JOB_STATUS:
                    try:
                        jobIds = req[1]
                        status = req[2]
                        recursive = req[3]
                        for jobId in jobIds:
                            loggerJobController.info("Received message set job status (job_id, status, recursive): "+str(jobId)+" "+str(status)+" "+str(recursive))
                            currentStatus = self.jobDAO.getJobStatus(jobId)
                            groupMembers = True
                            if currentStatus != status:
                                parentId = jobId
                                while parentId is not None:
                                    affectedJobs = self.updateJobStatus(parentId, status, recursive, groupMembers)
                                    for jId in affectedJobs:
                                        self.jobs.add(jId)
                                    if recursive:
                                        parentId = self.jobDAO.getParentId(parentId)
                                    else:
                                        parentId = None
                                    groupMembers = False
                        self.processActiveJobs()
                        if req[4] is not None:
                            self.jobDAO.sendResponse(req[4], True, "ok")
                    except Exception, e:
                        loggerJobController.exception(str(e))
                        if req[4] is not None:
                            self.jobDAO.sendResponse(req[4], False, e.message)
                        raise e
                elif messageType == DELETE_JOB:
                    try:
                        jobId = req[1]
                        loggerJobController.info("Received message delete job "+str(jobId))
                        j = self.jobDAO.getJobWithId(jobId)
                        if j.drmaaId is not None:
                            self.idToExecuter[j.executer].terminateJob(j.drmaaId)
                            self.jobDAO.updateDRMAAId(id, None)
                        self.jobDAO.deleteJob(jobId)
                        if req[2] is not None:
                            self.jobDAO.sendResponse(req[2], True, "ok")
                    except Exception, e:
                        loggerJobController.exception(str(e))
                        if req[2] is not None:
                            self.jobDAO.sendResponse(req[2], True, e.message)
                        raise e
                elif messageType == STOP:
                    loggerJobController.info("Received message stop")
                    self.running = False
            except Exception, e:
                loggerJobController.exception(str(e))
            finally:
                self.closeJobDAO()
        loggerJobController.info("stopped job manager")

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

def handleMessages(jobDAO, jobManager):
    transactionId = str(uuid4())
    try:
        messages = jobDAO.retreiveJobMessages(transactionId)
        for row in messages:
            messageType = row['type']
            if messageType == "launch":
                jobId = row['t_job_id']
                loggerMessageHandler.info("Received message start job "+str(jobId))
                jobManager.sendMessage([START_JOB, jobId, row['response_id']])
            elif messageType == "delete":
                jobId = row['t_job_id']
                loggerMessageHandler.info("Received message delete job "+str(jobId))
                jobManager.sendMessage([DELETE_JOB, jobId, row['response_id']])
            elif messageType == "status":
                jobId = row['t_job_id'];
                mess = row['message']
                vals = mess.split(":")
                status = vals[0]
                recursive = vals[1] == "True"
                loggerMessageHandler.info("Received message update job status (job_id, status, recursive): "+str(jobId)+", "+str(status)+", "+str(recursive))
                jobManager.sendMessage([SET_JOB_STATUS, [jobId], status, recursive, row['response_id']])
    except:
        jobDAO.removeMessageTransactionId(transactionId)
    finally:
        jobDAO.deleteMessagesWithId(transactionId)

class MessageHandlerProcess(threading.Thread):

    def __init__(self, jobManager):
        threading.Thread.__init__(self)
        self.daemon = True
        self.jobManager = jobManager
        self.running = True
        self.jobDAO = None

    def getOrCreateJobDAO(self):
        if self.jobDAO is None:
            self.jobDAO = createJobDAO()
        return self.jobDAO

    def stop(self):
        self.running = False

    def run(self):
        loggerMessageHandler.info("Started database message handler")
        self.getOrCreateJobDAO()
        while self.running:
            try:
                self.getOrCreateJobDAO()
                handleMessages(self.jobDAO, self.jobManager)
            except:
                traceback.print_exc()
            finally:
                self.jobDAO.db.close()
                self.jobDAO = None
                time.sleep(5)
        logging.info("Database message handler finished")

class Jobber():

    def __init__(self):
        self.running = False


    def start(self):
        self.running = True
        if not os.path.exists(Settings.logDir):
            os.makedirs(Settings.logDir)
        logging.basicConfig(filename=Settings.logDir+"/main.log", format='%(asctime)s %(message)s', level=logging.INFO)
        db = Connection.createDB()
        db.init()
        jobDAO = JobDAO.JobDAO(db)
        jobDAO.removeAllMessageTransactionIds()
        jobDAO.db.close()
        jobManager = JobManagerProcess()
        logging.info("starting job manager")
        jobManager.start()
        self.jobManager = jobManager
        messageHandler = MessageHandlerProcess(jobManager)
        logging.info("starting message handler")
        messageHandler.start()
        self.messageHandler = messageHandler

    def stop(self):
        logging.info("stopping job manager")
        self.jobManager.stop()
        self.messageHandler.stop()
        logging.info("stopping message handler")
        self.running = False
