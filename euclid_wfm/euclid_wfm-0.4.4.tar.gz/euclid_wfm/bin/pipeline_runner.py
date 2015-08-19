'''
Created on Apr 16, 2015

@author: martin.melchior
'''

import argparse
import logging
from uuid import uuid4

from euclidwf.utilities import config_loader, data_loader, visualizer
from euclidwf.framework.runner import PipelineExecution

logging.basicConfig(level=logging.DEBUG)

def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Test utility for loading and executing a pipeline.")
    parser.add_argument("--pipeline", help="Name of the python file that contains the pipeline specification.")
    parser.add_argument("--config", help="Path configuration file.")
    parser.add_argument("--data", help="Path to a file containing input data paths.")
    
    args = parser.parse_args()
    validate_args(parser, args)
    
    return args


def validate_args(parser, args):    
    pass
            

def load_configuration(configfile):
    config={}
    config_loader.load_config(configfile, config)
    return config
    

def load_inputs(datafile):
    data={}
    data_loader.load_data(datafile, data)
    return data


def main():
    args = parse_cmd_args()
    config=load_configuration(args.config)
    run={'runid'        : str(uuid4()),
         'config'       : config,
         'inputs'       : load_inputs(args.data),
         'pipeline'     : args.pipeline }

    pipeline_exec=PipelineExecution.fromdict(run)
    pipeline_exec.initialize()
    d = pipeline_exec.start()
            
    COL_NAMES=('TICK', 'MODEL PATH', 'PID', 'STATUS', 'DURATION', 'OUTPUT DIR')
    COL_WIDTH=(20,80,10,20,10,150)
    def print_report(result):
        print "".join(COL_NAMES[i].ljust(COL_WIDTH[i]) for i in range(len(COL_WIDTH)))
        for entries in pipeline_exec.report:
            line=[]
            for key in ['tick','path','pid','status','time','workdir']:
                if key=='time':
                    line.append("%.2f"%entries[key])
                else:
                    line.append(entries[key])
                    
            print "".join(line[i].ljust(COL_WIDTH[i]) for i in range(len(line)))
        return result

    def print_output_dict(result):
        if pipeline_exec.outputs:
            for portname, datapath in pipeline_exec.outputs.iteritems():
                print ''.join([portname.ljust(20), '-->'.ljust(5), datapath.ljust(80)])
        return result
    
    def visualize(result):
        g = pipeline_exec.traverser.get_graph()
        visualizer.visualize_graph(g)
        return result

    def failed_output(reason):
        print reason
        
    def stop_reactor(outputs):
        reactor.stop()

    d.addBoth(print_report)
    d.addBoth(print_output_dict)
    d.addErrback(failed_output)
    d.addBoth(visualize)
    d.addCallback(stop_reactor)
    from twisted.internet import reactor
    reactor.run()


if __name__ == '__main__':
    main()
