import os
import re
import types
import drmaa
from commandRunner import commandRunner


class geRunner(commandRunner.commandRunner):

    def __init__(self, **kwargs):
        self.args_set = []

        if "$OPTIONS" in kwargs['command']:
            raise ValueError("Grid Engine commands must be single exe names")
        if "$FLAGS" in kwargs['command']:
            raise ValueError("Grid Engine commands must be single exe names")
        if "$INPUT" in kwargs['command']:
            raise ValueError("Grid Engine commands must be single exe names")
        if "$OUTPUT" in kwargs['command']:
            raise ValueError("Grid Engine commands must be single exe names")
        if " " in kwargs['command']:
             raise ValueError("Grid Engine commands must be single exe names")
        commandRunner.commandRunner.__init__(self, **kwargs)

    def _translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # interpolate the file names if needed
        return(command)

    def prepare(self):
        '''
            Makes a directory and then moves the input data file there
        '''
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if self.input_data is not None:
            for key in self.input_data.keys():
                file_path = self.path+key
                fh = open(file_path, 'w')
                fh.write(self.input_data[key])
                fh.close()

        if self.input_string is not None:
            self.args_set.append(self.input_string)
        if self.flags is not None:
            self.args_set.extend(self.flags)
        if self.options is not None:
            [self.args_set.extend([k+" "+v]) for k, v in sorted(self.options.items())]

    def run_cmd(self, success_params=[0]):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        retval = None
        try:
            with drmaa.Session() as s:
                jt = s.createJobTemplate()
                jt.workingDirectory = self.path
                jt.outputPath = self.output_string
                jt.remoteCommand = self.command
                jt.args = self.args_set
                jt.joinFiles = False

                jobid = s.runJob(jt)

                retval = s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
                s.deleteJobTemplate(jt)
        except Exception as e:
            raise OSError("DRMAA session failed to execute: " + str(e))

        output_dir = os.listdir(self.path)

        if retval.exitStatus not in success_params:
            raise OSError("Exist status" + str(retval))

        self.output_data = {}
        for this_glob in self.out_globs:
            for outfile in output_dir:
                if outfile.endswith(this_glob):
                    with open(self.path+outfile, 'r') as content_file:
                        self.output_data[outfile] = content_file.read()

        return(retval.exitStatus)

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the tjmp dir
        '''
        for this_file in os.listdir(self.path):
            file_path = os.path.join(self.path, this_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(str(e))
        if os.path.exists(self.path):
            os.rmdir(self.path)
