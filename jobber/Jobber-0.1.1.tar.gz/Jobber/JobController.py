'''
Created on May 12, 2014

@author: rodak
'''
import logging

import threading
from Queue import Queue, Empty
import datetime
from time import sleep
import traceback
from uuid import uuid4
import time
import os

from . import database
from . import JobExecuter, Executers, Settings
from . import Logging

loggerJobController = Logging.logger("JobController", Settings.logDir+"/JobController.log")
loggerMessageHandler = Logging.logger("Message handler", Settings.logDir+"/MessageHandler.log")

class ExecutorMessageHandler(Executers.ResponseHandler):

    def __init__(self, controller):
        Executers.ResponseHandler.__init__(self)
        self.controller = controller

    def onExecutionId(self, jobId, executerId):
        loggerJobController.info("Job with id "+str(jobId)+" assigned execution id "+str(executerId))
        database.context(lambda db: database.dao(db).updateDRMAAId(jobId, executerId))


    def onJobFinished(self, executerId, error):
        db = database.getDB()
        dao = database.dao(db)
        try:
            drmaaId = executerId
            job = dao.getJobWithDrmaaId(drmaaId)
            loggerJobController.info("Job with execution id "+str(drmaaId)+" finished")
            if job is not None and job.status != database.jobStatus.CANCELLED:
                jobId = job.jobId
                loggerJobController.info("Job with id "+str(jobId)+" finished")
                status = database.jobStatus.FAILED
                dao.updateEndSubmitDate(jobId, datetime.datetime.now())
                startEnd = JobExecuter.readStartEndRun(job)
                if startEnd is not None:
                    dao.updateStartRunDate(jobId, datetime.datetime.fromtimestamp(startEnd['start']))
                    dao.updateEndRunDate(jobId, datetime.datetime.fromtimestamp(startEnd['end']))
                if error is None:
                    status = database.jobStatus.FINISHED
                    dao.updateError(jobId, "")
                else:
                    dao.updateError(jobId, error)
                if status == database.jobStatus.FAILED:
                    if dao.isRetryJob(jobId):
                        dao.updateJobStatus(jobId, database.jobStatus.IDLE)
                        self.controller.jobs.add(jobId)
                        self.controller.processActiveJobs()
                        return
                dao.updateJobStatus(jobId, status)
                self.controller.addAffectedJobs(jobId)
                self.controller.processActiveJobs()
                if job.parentId is None:
                    activable = dao.getActivableJob(job.name)
                    if activable is not None:
                        self.controller.launchJob(activable)
            else:
                if job is None:
                    loggerJobController.warn("Job with execution id "+str(drmaaId)+" not found")
        finally:
            database.releaseDB(db)


class JobManagerProcess(threading.Thread):

    def registerForUpdates(self, job):
        self.updateableJobs.append(job)

    def __init__(self):
        threading.Thread.__init__(self)
        self.processing = False
        self.daemon = True
        self.queue = Queue()
        self.groups = set()
        self.jobDAO = None
        self.running = True
        self.executer = Executers.create(ExecutorMessageHandler(self))

    def processActiveJobs(self):
        db = database.getDB()
        dao = database.dao(db)
        try:
            if self.processing:
                return
            self.processing = True
            while (len(self.jobs) > 0) or (len(self.groups) > 0):
                active = sorted(self.jobs)
                self.jobs = set([])
                for jobId in active:
                    self.chooseAction(jobId)
                    parent = dao.getParentId(jobId)
                    if parent is not None:
                        self.groups.add(parent)
                    else:
                        name = dao.getJobInfo(jobId)['name']
                        activable = dao.getActivableJob(name)
                        if activable is not None:
                            self.launchJob(activable)
                newGroups = set([])
                for gid in self.groups:
                    action = dao.getGroupJobAction(gid)
                    if action == database.jobAction.CANCEL:
                        dao.updateJobStatus(gid, database.jobStatus.CANCELLED)
                    elif action == database.jobAction.FAIL:
                        dao.updateJobStatus(gid, database.jobStatus.FAILED)
                    elif action == database.jobAction.FINISH_GROUP:
                        dao.updateJobStatus(gid, database.jobStatus.FINISHED)
                        for jid in dao.getAffectedJobs(gid):
                            self.jobs.add(jid)
                    elif action == database.jobAction.EXECUTE:
                        dao.updateJobStatus(gid, database.jobStatus.RUNNING)
                    elif action == database.jobAction.IDLE_GROUP:
                        dao.updateJobStatus(gid, database.jobStatus.IDLE)
                    if action != database.jobAction.NOTHING:
                        parent = dao.getParentId(gid)
                        if parent is not None:
                            newGroups.add(parent)
                        else:
                            name = dao.getJobInfo(gid)['name']
                            activable = dao.getActivableJob(name)
                            if activable is not None:
                                self.launchJob(activable)
                self.groups = newGroups
            self.processing = False
        finally:
            database.releaseDB(db)

    def stop(self):
        self.running = False
        self.queue.put(["stop"])
        self.executer.stop()

    def addAffectedJobs(self, jobId):
        db = database.getDB()
        dao = database.dao(db)
        try:
            for id in dao.getAffectedJobs(jobId):
                self.jobs.add(id)
            parent = dao.getParentId(jobId)
            if parent is not None:
                self.groups.add(parent)
        finally:
            database.releaseDB(db)

    def chooseAction(self, jobId):
        db = database.getDB()
        dao = database.dao(db)
        try:
            action = dao.getJobAction(jobId)
            if action == database.jobAction.EXECUTE:
                job = dao.getJobWithId(jobId)
                dao.updateStartSubmitDate(job.jobId, datetime.datetime.now())
                dao.updateJobStatus(job.jobId, database.jobStatus.RUNNING)
                dao.updateRun(job.jobId)
                job.currentRun += 1
                self.executer.run(job)
        finally:
            database.releaseDB(db)

    def sendMessage(self, mess):
        self.queue.put(mess)

    def updateStatus(self, jobIds, status, recursive, resonseId):
        self.queue.put(("update", jobIds, status, recursive, resonseId))

    def onUpdateStatus(self, jobIds, status, recursive, resonseId):
        db = database.getDB()
        dao = database.dao(db)
        try:
            for jobId in jobIds:
                loggerJobController.info("Received message set job status (job_id, status, recursive): "+str(jobId)+" "+str(status)+" "+str(recursive))
                currentStatus = dao.getJobStatus(jobId)
                groupMembers = True
                if currentStatus != status:
                    parentId = jobId
                    while parentId is not None:
                        affectedJobs = self._updateJobStatus(parentId, status, recursive, groupMembers)
                        for jId in affectedJobs:
                            self.jobs.add(jId)
                        if recursive:
                            parentId = dao.getParentId(parentId)
                        else:
                            parentId = None
                        groupMembers = False
            self.processActiveJobs()
            if resonseId is not None:
                dao.sendResponse(resonseId, True, "ok")
        except Exception, e:
            loggerJobController.exception(str(e))
            if resonseId is not None:
                dao.sendResponse(resonseId, False, e.message)
            raise e
        finally:
            database.releaseDB(db)

    def deleteJob(self, jobId, responseId):
        self.queue.put(("delete", jobId, responseId))

    def onDeleteJob(self, jobId, responseId):
        db = database.getDB()
        dao = database.dao(db)
        try:
            loggerJobController.info("Received message delete job "+str(jobId))
            j = dao.getJobWithId(jobId)
            if j.drmaaId is not None:
                self.executer.terminate(j.executer, j.drmaaId)
                dao.updateDRMAAId(id, None)
            dao.deleteJob(jobId)
            if responseId is not None:
                dao.sendResponse(responseId, True, "ok")
        except Exception, e:
            loggerJobController.exception(str(e))
            if responseId is not None:
                dao.sendResponse(responseId, False, e.message)
            raise e
        finally:
            database.releaseDB(db)

    def launchJob(self, jobId):
        db = database.getDB()
        dao = database.dao(db)
        try:
            if dao.getJobWithId(jobId) is None:
                loggerJobController.warn("job "+str(jobId)+" cannot be launched because it doesn't exist")
                return
            status = dao.getJobStatus(jobId)
            if status != database.jobStatus.DEACTIVATED or dao.canActivateJob(jobId):
                loggerJobController.info("activating job "+str(jobId))
                dao.activateJob(jobId)
                if dao.isGroupJob(jobId):
                    for jid in dao.getNoneGroupMembersRecursive(jobId):
                        self.jobs.add(jid)
                else:
                    self.jobs.add(jobId)
                self.processActiveJobs()
        finally:
            database.releaseDB(db)

    def startJob(self, jobId, responseId):
        self.queue.put(("start", jobId, responseId))

    def onStartJob(self, jobId, responseId):
        db = database.getDB()
        dao = database.dao(db)
        try:
            loggerJobController.info("Received message start job "+str(jobId))
            self.launchJob(jobId)
            if responseId is not None:
                dao.sendResponse(responseId, True, "ok")
        except Exception, e:
            loggerJobController.exception(str(e))
            if responseId is not None:
                dao.sendResponse(responseId, False, e.message)
            raise e
        finally:
            database.releaseDB(db)

    def _updateJobStatus(self, jobId, status, recursive, groupMembers):
        db = database.getDB()
        dao = database.dao(db)
        try:
            affectedJobs = set()
            job = dao.getJobWithId(jobId)
            if not job.groupJob:
                affectedJobs.add(jobId)
            if job.status != status:
                if job.groupJob and (status != database.jobStatus.FINISHED or job.status != database.jobStatus.RUNNING) and groupMembers:
                    for mId in dao.getGroupMemebers(jobId):
                        affectedJobs.add(mId)
                        self._updateJobStatus(mId, status, recursive, groupMembers)
                if status == database.jobStatus.IDLE or status == database.jobStatus.CANCELLED:
                    if not job.groupJob and job.status == database.jobStatus.RUNNING:
                        self.executer.terminate(job.executer, job.drmaaId)
                        dao.updateDRMAAId(jobId, None)
                    dao.updateJobStatus(jobId, status)
                elif status == database.jobStatus.FINISHED:
                    if job.status != database.jobStatus.RUNNING:
                        dao.updateJobStatus(jobId, status)
            if recursive:
                depJobIds = dao.getDependentJobs(jobId)
                for depId in depJobIds:
                    for affId in self._updateJobStatus(depId, status, recursive, True):
                        affectedJobs.add(affId)
            return affectedJobs
        finally:
            database.releaseDB(db)

    def respond(self, response_id, message):
        database.context(lambda db: database.dao(db).sendResponse(response_id, message))

    def run(self):
        loggerJobController.info("started job manager")
        db = database.getDB()
        dao = database.dao(db)
        running = dao.getRunningJobIds()
        dao.setRunningJobsToIdle()
        for id in running:
            j = dao.getJobWithId(id)
            if j.drmaaId is not None:
                self.executer.terminate(j.executer, j.drmaaId)
                dao.updateDRMAAId(id, None)
        self.jobs = set(dao.getActiveJobIds())
        self.processActiveJobs()
        database.releaseDB(db)
        while self.running:
            try:
                nr = 0
                while nr < 100:
                    nr += 1
                    req = self.queue.get(False)
                    messageType = req[0]
                    if messageType == "start":
                        self.onStartJob(req[1], req[2])
                    elif messageType == "update":
                        self.onUpdateStatus(req[1], req[2], req[3], req[4])
                    elif messageType == "delete":
                        self.onDeleteJob(req[1], req[2])
                    elif messageType == "stop":
                        loggerJobController.info("Received message stop")
                        self.running = False
            except Empty:
                pass
            except Exception, e:
                loggerJobController.exception(str(e))

            try:
                self.executer.handleMessages()
            except Exception, e:
                loggerJobController.exception(str(e))
            sleep(0.2)
        loggerJobController.info("stopped job manager")
        self.executer.stop()



def handleMessages(jobDAO, jobManager):
    transactionId = str(uuid4())
    try:
        messages = jobDAO.retreiveJobMessages(transactionId)
        for row in messages:
            messageType = row['type']
            if messageType == "launch":
                jobId = row['t_job_id']
                loggerMessageHandler.info("Received message start job "+str(jobId))
                jobManager.startJob(jobId, row['response_id'])
            elif messageType == "delete":
                jobId = row['t_job_id']
                loggerMessageHandler.info("Received message delete job "+str(jobId))
                jobManager.deleteJob(jobId, row['response_id'])
            elif messageType == "status":
                jobId = row['t_job_id']
                mess = row['message']
                vals = mess.split(":")
                status = vals[0]
                recursive = vals[1] == "True"
                loggerMessageHandler.info("Received message update job status (job_id, status, recursive): "+str(jobId)+", "+str(status)+", "+str(recursive))
                jobManager.updateStatus([jobId], status, recursive, row['response_id'])
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

    def stop(self):
        self.running = False

    def run(self):
        loggerMessageHandler.info("Started database message handler")
        while self.running:
            db = database.getDB()
            try:
                dao = database.dao(db)
                handleMessages(dao, self.jobManager)
            except:
                traceback.print_exc()
            finally:
                database.releaseDB(db)
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
        db = database.getDB()
        db.init()
        jobDAO = database.dao(db)
        jobDAO.removeAllMessageTransactionIds()
        database.releaseDB(db)
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
