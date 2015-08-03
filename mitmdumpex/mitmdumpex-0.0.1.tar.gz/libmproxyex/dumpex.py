from libmproxy import flow
from libmproxy.dump import *
from .splitflowwriter import SplitFlowWriter

class DumpExMaster(DumpMaster):
    def __init__(self, server, options, outfile=sys.stdout):
        # Delay the stream setup, otherwise it gets overwriten by FlowMaster.__init__
        split_dir = None
        if options.outfile and options.outfile[1] == 'split-flows':
            split_dir = options.outfile[0]
            options.outfile = None

        # Delay the flows loading, otherwise we can't use our custom FlowWriter
        rfile = None
        if options.rfile:
            rfile = options.rfile
            options.rfile = None

        super(DumpExMaster, self).__init__(server, options, outfile)

        if split_dir:
            self.start_split_stream(split_dir, self.filt)

        if rfile:
            options.rfile = rfile
            try:
                self.load_flows_file(options.rfile)
            except flow.FlowReadError as v:
                self.add_event("Flow file corrupted.", "error")
                raise DumpError(v)


    def start_split_stream(self, split_dir, filt):
        self.stream = SplitFlowWriter(split_dir, flow.FilteredFlowWriter, [filt])


    def stop_stream(self):
        if hasattr(self.stream, 'close'):
            self.stream.close()
        else:
            super(DumpExMaster, self).stop_stream(self)

