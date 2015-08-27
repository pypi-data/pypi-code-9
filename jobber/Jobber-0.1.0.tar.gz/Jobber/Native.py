from Queue import Queue, Empty
from subprocess import Popen
import threading
import time
from time import sleep
import os
import sys
import uuid

__author__ = 'rodak'

class BashJob():

    def __init__(self, stdout, stderr, script):
        self.script = script
        if stdout is not None:
            self.out = open(stdout, "w")
        else:
            self.out = None
        if stderr is not None:
            self.err = open(stderr, "w")
        else:
            self.err = None
        self.process = Popen([self.script], stdout=self.out, stderr=self.err, shell=True)

    def poll(self):
        return self.process.poll()

    def wait(self):
        return self.process.wait()

    def kill(self):
        self.process.kill()

EXECUTE=0
KILL=1
STOP=2

class ExecuterMessage():

    def __init__(self, type, message):
        self.type = type
        self.message = message

class RunJobMessage():

    def __init__(self, script, stdout, stderr, resultListener):
        self.script = script
        self.stdout = stdout
        self.stderr = stderr
        self.resultListener = resultListener
        self.maxRuntime = 10
        self.message = None
        self.jobId = None


RUNNING=0
FINISHED=1
TIMEOUT=2
KILLED=3

class RunJobResults():

    def __init__(self, status, returnCode, jobId):
        self.status = status
        self.returnCode = returnCode
        self.jobId = jobId

class SingleSystemCommandExecuter():

    def __init__(self, job, maxRuntime, listener, jobId):
        self.job = job
        self.jobId = jobId
        self.startTime = time.time()
        self.maxRuntime = maxRuntime
        self.listener = listener

    def checkJob(self):
        res = self.job.poll()
        if res is None:
            currentTime = time.time()
            runtime = currentTime - self.startTime
            if runtime > self.maxRuntime:
                try:
                    self.job.kill()
                    self.job.wait()
                except OSError:
                    pass
                self.listener(RunJobResults(TIMEOUT, None, self.jobId))
                return TIMEOUT
        else:
            self.listener(RunJobResults(FINISHED, res, self.jobId))
            return FINISHED
        return RUNNING

    def killJob(self):
        try:
            self.job.kill()
            self.job.wait()
        except OSError:
            pass
        self.listener(RunJobResults(KILLED, None, self.jobId))

def runOrDie(command):
    ret = os.system(command)
    if ret != 0:
        sys.stderr.write("Running command failed: "+command+"\n")
        sys.exit(ret)

class SystemCommandPooledExecuter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.poolSize = 6
        self.running = True
        self.queue = Queue()
        self.lock = threading.RLock()

    def execute(self, jobMessage):
        self.lock.acquire()
        try:
            jobId = str(uuid.uuid4())
            jobMessage.jobId = jobId
            self.queue.put(ExecuterMessage(EXECUTE, jobMessage))
            return jobId
        finally:
            self.lock.release()

    def kill(self, jobId):
        self.queue.put(ExecuterMessage(KILL, jobId))

    def run(self):
        idToExecuting = {}
        idToExecute = {}
        while self.running:
            try:
                message = self.queue.get(False)
                if message is not None:
                    if message.type == EXECUTE:
                        idToExecute[message.message.jobId] = message.message
                    elif message.type == KILL:
                        jobId = message.message
                        if jobId in idToExecute:
                            message = idToExecute[jobId]
                            del idToExecute[jobId]
                            message.resultListener(RunJobResults(KILLED, None, message.jobId))
                        elif jobId in idToExecuting:
                            ex = idToExecuting[jobId]
                            del idToExecuting[jobId]
                            ex.killJob()
                    elif message.type == STOP:
                        self.running = False
                        break
            except Empty:
                pass
            for jobId in idToExecuting.keys():
                ex = idToExecuting[jobId]
                j = ex.checkJob()
                if j != RUNNING:
                    del idToExecuting[jobId]
            while len(idToExecuting) < self.poolSize and len(idToExecute) > 0:
                key = idToExecute.iterkeys().next()
                message = idToExecute[key]
                del idToExecute[key]
                idToExecuting[key] = SingleSystemCommandExecuter(BashJob(message.stdout, message.stderr, message.script), message.maxRuntime, message.resultListener, key)
            sleep(0.3)


    def stop(self):
        self.running = False
        self.queue.put(ExecuterMessage(STOP, None))
