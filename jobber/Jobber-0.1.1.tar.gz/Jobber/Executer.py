import Queue
from Queue import Empty
import threading
from time import sleep
from Jobber import Settings, Logging

__author__ = 'rodak'


logger = Logging.logger("Executer", Settings.logDir+"/Executer.log")

class Executer(threading.Thread):

    def __init__(self, response):
        threading.Thread.__init__(self)
        self.response = response
        self.queue = Queue.Queue()
        self.batchNr = 100

    def terminate(self, executerId):
        self.queue.put(("terminate", executerId))

    def execute(self, job, script, logDir):
        self.queue.put(("execute", job, script, logDir))

    def status(self, executerId):
        self.queue.put("status", executerId)

    def stop(self):
        self.queue.put(["stop"])

    def onTerminate(self, jobId):
        raise Exception("onTerminate must be implemented by subclasses")

    def onExecute(self, job, script, logDir):
        raise Exception("onExecute must be implemented by subclasses")

    def onStatus(self):
        raise Exception("onStatus must be implemented by subclasses")

    def onStop(self):
        pass

    def onRun(self):
        pass

    def run(self):
        running = True
        while running:
            try:
                try:
                    nr = 0
                    while nr < self.batchNr:
                        nr += 1
                        mess = self.queue.get(False)
                        if mess[0] == "terminate":
                            self.onTerminate(mess[1])
                        elif mess[0] == "execute":
                            self.onExecute(mess[1], mess[2], mess[3])
                        elif mess[0] == "stop":
                            running = False
                            self.onStop()
                            return
                except Empty:
                    pass
                self.onRun()
            except Exception, e:
                logger.exception(str(e))
            sleep(0.2)
