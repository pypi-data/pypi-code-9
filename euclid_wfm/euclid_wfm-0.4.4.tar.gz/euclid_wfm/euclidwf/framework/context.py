'''
Created on Apr 30, 2015

@author: martin.melchior (at) fhnw.ch
'''
import os
from euclidwf.utilities import file_transporter
from euclidwf.framework.configuration import LOCALCACHE, WS_ROOT,\
    DRM_CHECKSTATUS_TIME, DRM_CHECKSTATUS_TIMEOUT

CONTEXT='context'
WORKDIR='workdir'
LOGDIR='logdir'
LOCALWORKDIR='local_workdir'
TRANSPORTER='transporter'
CHECKSTATUS_TIME="check_status.polltime"
CHECKSTATUS_TIMEOUT="check_status.timeout"

def create_context(data, config):
    context={}
    context[WORKDIR]=os.path.join(config[WS_ROOT],data[WORKDIR])
    context[LOGDIR]=os.path.join(config[WS_ROOT],data[LOGDIR])
    context[LOCALWORKDIR]=os.path.join(config[LOCALCACHE],data[WORKDIR])
    context[TRANSPORTER]=file_transporter.create(config)
    context[CHECKSTATUS_TIME]=float(config[DRM_CHECKSTATUS_TIME])
    context[CHECKSTATUS_TIMEOUT]=float(config[DRM_CHECKSTATUS_TIMEOUT])
    return context


def serializable(context):
    return {k:v for k,v in context.iteritems() if k!=TRANSPORTER}
