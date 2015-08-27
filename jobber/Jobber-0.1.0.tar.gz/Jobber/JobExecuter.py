import os
from . import Settings

__author__ = 'rodak'


JOB_FINISHED = "Finished"

class JobAndScript():

    def __init__(self, job, script, logDir):
        self.job = job
        self.script = script
        self.logDir = logDir

class DRMAAResponse():

    def __init__(self, messType, message):
        self.type = messType
        self.message = message

class JobIdParts():

    def __init__(self, first, second, third, jobId):
        self.first = first
        self.second = second
        self.third = third
        self.jobId = jobId

    def getPath(self):
        return self.first+"/"+self.second+"/"+self.third

    def __str__(self):
        return self.getPath()

def jobIdToParts(jobId):
    sid = str(jobId)
    if len(sid) > 3:
        if len(sid) > 6:
            third = sid[-3:]
            second = sid[-6: -3]
            first = sid[:len(sid) - 6]
            return JobIdParts(first, second, third, jobId)
        else:
            third = sid[-3:]
            second = sid[:len(sid) - 3]
            return JobIdParts("0", second, third, jobId)
    else:
        return JobIdParts("0", "0", sid, jobId)

def createLogDir(job):
    parts = jobIdToParts(job.jobId)
    logDir = Settings.logDir+"/"+parts.getPath()+"/"+str(job.currentRun)
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    return logDir

def readStartEndRun(job):
    logDir = createLogDir(job)
    if not os.path.exists(logDir+"/start"):
        return None
    if not os.path.exists(logDir+"/end"):
        return None
    with open(logDir+"/start") as f:
        try:
            start = long(f.read())
        except:
            return None
    with open(logDir+"/end") as f:
        try:
            end = long(f.read())
        except:
            return None
    return {
        'start': start,
        'end': end
    }

def createRunScript(job):
    modules = []
    for opt in job.options:
        if opt.name == 'module':
            modules.append(opt.value)
    logDir = createLogDir(job)
    w = open(logDir+"/command.sh", "w")
    w.write("#!/bin/bash\n\n")
    for mod in modules:
        w.write("module load "+mod+"\n")
    w.write("\n")
    w.write("date +%s > "+logDir+"/start\n")
    w.write(job.command+"\n")
    w.write("exitStatus=$?\n")
    w.write("date +%s > "+logDir+"/end\n")
    w.write("exit ${exitStatus}\n")
    w.close()
    os.chmod(logDir+"/command.sh", 0777)
    return logDir+"/command.sh"
