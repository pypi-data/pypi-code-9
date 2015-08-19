'''
Created on Jun 2, 2015

@author: martin.melchior
'''
import json
from euclidwf.framework.configuration import DRM_CONFIGURE, DRM_SUBMIT,\
    DRM_CHECKSTATUS, DRM_CLEANUP, DRM_CANCEL, DRM_PROTOCOL, DRM_HOSTNAME, \
    WS_PROTOCOL, WS_HOSTNAME, WS_ROOT, LOCALCACHE, WFM_PROXYFCTS, WFM_PKGDEFS, \
    WFM_SCRIPTS
from euclidwf.server import server_config
import os


def load_submit_data(payload, servercfg):
    data=convert(json.loads(payload))
    data=add_server_config(data, servercfg)
    return data


def add_server_config(data, servercfg):
    config=data['config']
    config[DRM_CONFIGURE]=servercfg[server_config.DRM_CONFIGURE]
    config[DRM_SUBMIT]=servercfg[server_config.DRM_SUBMIT]
    config[DRM_CHECKSTATUS]=servercfg[server_config.DRM_CHECKSTATUS]
    config[DRM_CLEANUP]=servercfg[server_config.DRM_CLEANUP]
    config[DRM_CANCEL]=servercfg[server_config.DRM_CANCEL]
    config[DRM_PROTOCOL]=servercfg[server_config.DRM_PROTOCOL]
    config[DRM_HOSTNAME]=servercfg[server_config.DRM_HOSTNAME]

    config[WS_PROTOCOL]=servercfg[server_config.WS_PROTOCOL]
    config[WS_HOSTNAME]=servercfg[server_config.WS_HOSTNAME]
    config[WS_ROOT]=servercfg[server_config.WS_ROOT]

    config[LOCALCACHE]=servercfg[server_config.LOCALCACHE]

    config[WFM_PROXYFCTS]=os.path.join(servercfg[server_config.WFM_PROXYFCTS_ROOT],config[WFM_PROXYFCTS])
    config[WFM_PKGDEFS]=os.path.join(servercfg[server_config.WFM_PKGDEFS_ROOT],config[WFM_PKGDEFS])
    config[WFM_SCRIPTS]=os.path.join(servercfg[server_config.WFM_SCRIPTS_ROOT],config[WFM_SCRIPTS])
    
    return data


def convert(obj):
    if isinstance(obj, dict):
        return {k:convert(v) for k,v in obj.iteritems()}
    elif isinstance(obj, list):
        return [convert(v) for v in obj]
    elif isinstance(obj, unicode):
        return str(obj)
    else:
        return obj
        


class PipelineRunRegistry():        
    
    def __init__(self):
        self.registry = {}

    def has_run(self, runid):
        return runid in self.registry.keys()
    
    def add_run(self, runid, pipelinerun):
        if runid not in self.registry.keys():
            self.registry[runid]=pipelinerun
        else:
            raise RuntimeError("Runid %s already exists."%runid)

    def get_all_runids(self):
        return [runid for runid in self.registry.keys()]
    
    def get_run(self, runid):
        if runid in self.registry.keys():
            return self.registry[runid]
        else:
            raise RuntimeError("Runid %s does not exist in the registry."%runid)

    def get_run_status(self, runid):
        if runid in self.registry.keys():
            return self.registry[runid].status
        else:
            return None

    def delete_run(self, runid): 
        if runid in self.registry.keys():
            del self.registry[runid]
        if runid in self.registry.keys():
            raise RuntimeError("Runid %s could not be removed from registry."%runid)
            

class PipelineRunServerHistory():
    
    def __init__(self):
        self.history = []

    def add_entry(self, msg, datetime):
        self.history.append((msg,datetime))


registry = PipelineRunRegistry()
history=PipelineRunServerHistory()

