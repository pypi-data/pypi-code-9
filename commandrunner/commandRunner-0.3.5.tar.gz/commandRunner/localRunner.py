import os
import re
import types
from commandRunner import commandRunner
from subprocess import call


class localRunner(commandRunner.commandRunner):

    def __init__(self, **kwargs):
        commandRunner.commandRunner.__init__(self, **kwargs)

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

    def run_cmd(self, success_params=[0]):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        exit_status = None
        os.chdir(self.path)
        try:
            exit_status = call(self.command, shell=True)
        except Exception as e:
            raise OSError("call() attempt failed")

        output_dir = os.listdir(self.path)

        if exit_status not in success_params:
            raise OSError("Exist status" + str(exit_status))

        self.output_data = {}
        for this_glob in self.out_globs:
            for outfile in output_dir:
                if outfile.endswith(this_glob):
                    with open(self.path+outfile, 'r') as content_file:
                        self.output_data[outfile] = content_file.read()

        return(exit_status)

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the temp dir
        '''
        for this_file in os.listdir(self.path):
            file_path = os.path.join(self.path, this_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        if os.path.exists(self.path):
            os.rmdir(self.path)
