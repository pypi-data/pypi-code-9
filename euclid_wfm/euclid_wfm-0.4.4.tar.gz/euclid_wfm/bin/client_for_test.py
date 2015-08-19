'''
Created on May 27, 2015

@author: martin.melchior
'''
import argparse
import httplib
import json
from euclidwf.utilities import data_loader
from euclidwf.framework.configuration import WFM_PKGDEFS, WFM_PROXYFCTS,\
    WFM_SCRIPTS, DRM_USERNAME, DRM_PASSWORD, WS_USERNAME, WS_PASSWORD,\
    DRM_CHECKSTATUS_TIME, DRM_CHECKSTATUS_TIMEOUT

def load_run_request_spe(runid):
    data = {}
    data['runid']=str(runid)
    data['pipeline']="spe_test_pipeline.py"
    config={}
    config[DRM_USERNAME]='sgsst'
    config[DRM_PASSWORD]='euclid'
    config[WS_USERNAME]='sgsst'
    config[WS_PASSWORD]='euclid'
    config[WFM_PKGDEFS]='pkgdefs'
    config[WFM_PROXYFCTS]='packages'
    config[WFM_SCRIPTS]='examples'
    config[DRM_CHECKSTATUS_TIME]=5.0
    config[DRM_CHECKSTATUS_TIMEOUT]=7200
    data['config']=config
    inputs={}
    datafile="/Users/martinm/Projects/euclid/pipeline_framework/prototype/wfm/trunk/euclidwf_examples/resources/spe_test.data"
    data_loader.load_data(datafile, inputs)
    inputs['workdir']="%s_%s"%(inputs['workdir'],runid)
    inputs['logdir']="%s/logdir"%(inputs['workdir'])
    data['inputs']=inputs
    return json.dumps(data)

def load_run_request_vis(runid):
    data = {}
    data['runid']=str(runid)
    data['pipeline']="vis_pipeline.py"
    config={}
    config[DRM_USERNAME]='sgsst'
    config[DRM_PASSWORD]='euclid'
    config[WS_USERNAME]='sgsst'
    config[WS_PASSWORD]='euclid'
    config[WFM_PKGDEFS]='pkgdefs'
    config[WFM_PROXYFCTS]='packages'
    config[WFM_SCRIPTS]='examples'
    config[DRM_CHECKSTATUS_TIME]=5.0
    config[DRM_CHECKSTATUS_TIMEOUT]=7200
    data['config']=config
    inputs={}
    datafile="/Users/martinm/Projects/euclid/pipeline_framework/prototype/wfm/trunk/euclidwf_examples/resources/vis_pipeline.data"
    data_loader.load_data(datafile, inputs)
    inputs['workdir']="%s_%s"%(inputs['workdir'],runid)
    inputs['logdir']="%s/logdir"%(inputs['workdir'])
    data['inputs']=inputs
    return json.dumps(data)


def load_run_request_test(runid):
    data = {}
    data['pipeline']="vis_pipeline.py"
    config={}
    config[DRM_USERNAME]='sgsst'
    config[DRM_PASSWORD]='euclid'
    config[WS_USERNAME]='sgsst'
    config[WS_PASSWORD]='euclid'
    config[WFM_PKGDEFS]='pkgdefs'
    config[WFM_PROXYFCTS]='packages'
    config[WFM_SCRIPTS]='examples'
    config[DRM_CHECKSTATUS_TIME]=5.0
    config[DRM_CHECKSTATUS_TIMEOUT]=7200
    data['config']=config
    inputs={}
    datafile="/Users/martinm/Projects/euclid/pipeline_framework/prototype/wfm/trunk/euclidwf_examples/resources/vis_pipeline.data"
    data_loader.load_data(datafile, inputs)
    inputs['workdir']="%s_%s"%(inputs['workdir'],runid)
    inputs['logdir']="%s/logdir"%(inputs['workdir'])
    data['inputs']=inputs
    return json.dumps(data)

def submit(runid, pipeline):
    if pipeline=='vis':
        jsondata = load_run_request_vis(runid)
    elif pipeline=='spe':
        jsondata = load_run_request_spe(runid)
    elif pipeline=='test':
        jsondata = load_run_request_test(runid)
    else:
        return
    connection = httplib.HTTPConnection(host='localhost', port=10000)
    headers = {'Content-type': 'application/json'}
    connection.request('POST', '/submit', jsondata, headers)
    return connection.getresponse()
    

def status(runid):
    connection = httplib.HTTPConnection(host='localhost', port=10000)
    headers = {'Content-type': 'application/json'}
    jsondata=json.dumps({'runid':runid})
    connection.request('GET', '', jsondata, headers)
    return connection.getresponse()
    

def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Test application for submitting and status checks for the pipeline server.")
    parser.add_argument("--type", help="POST | GET | PUT | DELETE")
    parser.add_argument("--runids", nargs='+', help="RunIds.")    
    parser.add_argument("--runid", help="RunId.")
    parser.add_argument("--pipeline", help="Pipeline.")
    
    return parser.parse_args()    


if __name__ == '__main__':
    args = parse_cmd_args()
    
    if args.type=='POST':
        for runid in args.runids:
            response=submit(runid, args.pipeline)
            print '\n'.join(response.read().decode().splitlines())
    elif args.type=='GET':
        response=status(args.runid)
        print '\n'.join(response.read().decode().splitlines())
        