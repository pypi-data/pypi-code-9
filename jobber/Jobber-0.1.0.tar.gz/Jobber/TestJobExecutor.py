import Queue
from Queue import Empty
import threading
from time import sleep
from .JobExecuter import DRMAAResponse, JOB_FINISHED

__author__ = 'rodak'

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

class TestExecuter(threading.Thread):

    def __init__(self, results):
        self.results = results
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.running = True

    def start(self):
        super(TestExecuter, self).start()

    def runJob(self, job, listener):
        self.queue.put(JobMessage(EXECUTE_JOB, RunJob(job, listener)))

    def stop(self):
        self.running = False
        self.queue.put(JobMessage(STOP, None))

    def terminateJob(self, jobId):
        self.queue.put(JobMessage(TERMINATE_JOB, jobId))

    def run(self):
        try:
            while self.running:
                wait = True
                try:
                    mess = self.queue.get(False)
                    wait = False
                    if mess.type == EXECUTE_JOB:
                        self.results(DRMAAResponse(JOB_FINISHED, 0))
                    elif mess.type == JOB_STATUS:
                        jobId = mess.message
                        jobStatus = "unknown"
                        mess.message.listener(jobStatus)
                    elif mess.type == TERMINATE_JOB:
                        jobId = mess.message
                    elif mess.type == STOP:
                        self.running = False
                        break
                except Empty:
                    pass
                if wait:
                    sleep(0.2)
        finally:
            pass
