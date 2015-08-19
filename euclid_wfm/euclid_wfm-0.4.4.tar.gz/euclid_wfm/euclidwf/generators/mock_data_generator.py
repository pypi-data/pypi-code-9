'''
Created on Apr 25, 2015

@author: martin.melchior
'''
import argparse
import imp
import os
import sys

from pydron.dataflow.graph import START_TICK

from euclidwf.framework.context import CONTEXT
from euclidwf.framework.graph_builder import PydronGraphBuilder


def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Utility generating mock data for testing.")
    parser.add_argument("--pipeline", help="Source files that contains the pipeline specification.")
    parser.add_argument("--pipelinename", help="Name of pipeline - should correspond to the name of the method that specifies the pipeline.")
    parser.add_argument("--path", nargs='+', help="Directories to be added to PYTHONPATH dynamically.")
    parser.add_argument("--destdir", help="Directory to write the test data to.")
    parser.add_argument("--workdir", help="Workdir mentioned in the pipeline input data file.")
    parser.add_argument("--logdir", help="Logdir mentioned in the pipeline input data file.")
    args = parser.parse_args()
    
    return args

def create_mock_data(inputname, consumers, destdir):
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    inputfilename=inputname+".dat"
    inputfilepath=os.path.join(destdir, inputfilename)
    with open(inputfilepath, 'w') as inputfile:
        inputfile.write("Mock data for input port %s.\n"%inputname)
        for portname,nodepath in consumers:
            inputfile.write("Consumed by node %s at port %s.\n"%(nodepath,portname))
    return inputfilename
            

def get_mock_inputs(pipeline_spec, destdir):
    pipeline_spec.isroot=True
    builder=PydronGraphBuilder(pipeline_spec)
    builder.build()
    inputs={}
    for source,dest in builder.graph.get_out_connections(START_TICK):
        if source.port==CONTEXT:
            continue
        if source.port not in inputs.keys():
            inputs[source.port]=[]
        nodepath=builder.graph.get_task_properties(dest.tick)['path']
        inputs[source.port].append((dest.port,nodepath))
    
    for inputname, consumers in inputs.iteritems():
        inputs[inputname]=create_mock_data(inputname, consumers, destdir)
    
    return inputs


def pipeline_spec(pipelinefile, pipelinename):
    filename=os.path.basename(pipelinefile)
    pipeline_module_name,_=os.path.splitext(filename)
    pipeline_module=imp.load_source(pipeline_module_name, pipelinefile)
    return getattr(pipeline_module, pipelinename)
    

def create_pipeline_data_file(inputs, filename, destdir, workdir, logdir):
    inputfilepath=os.path.join(destdir,filename)+".dat"
    with open(inputfilepath, 'w') as inputfile:
        inputfile.write("workdir=%s\n"%workdir)
        inputfile.write("logdir=%s\n"%logdir)
        for inputname, filename in inputs.iteritems():
            inputfile.write("%s=%s\n"%(inputname,filename))
            

def add_to_path(locations):
    if not locations:
        return
    for loc in locations:
        sys.path.append(loc)


def main():
    args = parse_cmd_args()
    add_to_path(args.path)
    spec=pipeline_spec(args.pipeline, args.pipelinename)
    inputs=get_mock_inputs(spec, args.destdir)
    create_pipeline_data_file(inputs, args.pipelinename, args.destdir, args.workdir, args.logdir)
    


if __name__ == '__main__':
    main()
