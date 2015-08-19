'''
Created on Apr 27, 2015

@author: martin.melchior
'''
from euclidwf.framework.context import WORKDIR, LOGDIR

DRM_TASK="--task=%s"
DRM_WORKDIR="--workdir=%s"
DRM_LOGDIR="--logdir=%s"
DRM_INPUTS="--inputs=%s"
DRM_OUTPUTS="--outputs=%s"

def submit_cmd_as_list(submit_cmd, task, workdir, logdir, inputs, outputs):
    cmdArray = submit_cmd.split()
    cmdArray.append(DRM_TASK%task)
    cmdArray.append(DRM_WORKDIR%workdir)
    cmdArray.append(DRM_INPUTS%str(inputs))
    cmdArray.append(DRM_OUTPUTS%str(outputs))
    cmdArray.append(DRM_LOGDIR%logdir)       
    return cmdArray


def create_command(submit_name, taskname, inputs, outputs, context):
    return submit_cmd_as_list(submit_name, taskname, context[WORKDIR], context[LOGDIR], inputs, outputs)


JOB_PENDING = "PENDING"
JOB_QUEUED = "QUEUED"
JOB_EXECUTING = "EXECUTING"
JOB_COMPLETED = "COMPLETED"
JOB_ERROR = "ERROR"
JOB_UNKNOWN = "UNKNOWN"
JOB_HELD = "HELD"
JOB_SUSPENDED = "SUSPENDED"
JOB_ABORTED = "ABORTED"

waiting_state=(JOB_PENDING, JOB_QUEUED, JOB_EXECUTING, JOB_HELD)
error_state=(JOB_ERROR, JOB_UNKNOWN, JOB_SUSPENDED, JOB_ABORTED)
success_state=(JOB_COMPLETED,)

#EXIT CODES
E_SUCCESS = 0
E_INPUTERROR = 1
E_INVALIDCONFIG = 2
E_IOERROR = 3
E_GENERICERROR = -1

def wait_for_job(state):
    return state in waiting_state

def job_completed(state):
    return state in success_state

def job_failed(state):
    return state in error_state
