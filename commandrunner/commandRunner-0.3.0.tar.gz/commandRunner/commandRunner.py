import os
import re
import types
from subprocess import call


class commandRunner():

    def __init__(self, **kwargs):
        '''
            Constructs a local job
            takes
            tmp_id = string
            tmp_path="/tmp/"
            command="ls /tmp > $OUTPUT"

            out_globs=['file',]
            input_data={filename:data_string}
            input_string="test.file"
            output_string="out.file"
            options = {flag:entry}
            flags = [strings,]
        '''
        self.tmp_id = None
        self.tmp_path = None
        self.out_globs = None
        self.command = None
        self.input_data = None
        self.command = None

        self.input_string = None
        self.output_string = None
        self.options = None
        self.flags = None
        self.output_data = None
        self.path = None

        self.__check_arguments(kwargs)

        self.tmp_path = re.sub("/$", '', self.tmp_path)
        self.path = self.tmp_path+"/"+self.tmp_id+"/"
#       self.command = self.__translate_command(kwargs.pop('command', ''))
        self.command = self._translate_command(self.command)

    def __check_arguments(self, kwargs):
        # flags = (strings,)
        if os.path.isdir(kwargs['tmp_path']):
            self.tmp_path = kwargs.pop('tmp_path', '')
        else:
            raise OSError('tmp_path provided does not exist')

        if isinstance(kwargs['tmp_id'], str):
            self.tmp_id = kwargs.pop('tmp_id', '')
        else:
            raise TypeError('tmp_id must be a string')

        if isinstance(kwargs['command'], str):
            self.command = kwargs.pop('command', '')
        else:
            raise TypeError('command must be a string')

        if 'input_data' in kwargs:
            if isinstance(kwargs['input_data'], dict):
                self.input_data = kwargs.pop('input_data', '')
            else:
                raise TypeError('input_data must be a dict')

        if 'out_globs' in kwargs:
            if isinstance(kwargs['out_globs'], list):
                self.out_globs = kwargs.pop('out_globs', '')
            else:
                raise TypeError('out_globs must be array')

        if 'input_string' in kwargs:
            if isinstance(kwargs['input_string'], str):
                self.input_string = kwargs.pop('input_string', '')
            else:
                raise TypeError('input_string must be str')
        if 'output_string' in kwargs:
            if isinstance(kwargs['output_string'], str):
                self.output_string = kwargs.pop('output_string', '')
            else:
                raise TypeError('output_string must be str')

        if 'options' in kwargs:
            if isinstance(kwargs['options'], dict):
                self.options = kwargs.pop('options', '')
            else:
                raise TypeError('options must be dict')

        if 'flags' in kwargs:
            if isinstance(kwargs['flags'], list):
                self.flags = kwargs.pop('flags', '')
            else:
                raise TypeError('flags must be list')

        if "$OPTIONS" in self.command and self.options is None:
            raise ValueError("Command string references $OPTIONS but no"
                             "options provided")
        if "$FLAGS" in self.command and self.flags is None:
            raise ValueError("Command string references $FLAGS but no"
                             "flags provided")
        if "$INPUT" in self.command and self.input_string is None:
            raise ValueError("Command string references $INPUT but no"
                             "input_string provided")
        if "$OUTPUT" in self.command and self.output_string is None:
            raise ValueError("Command string references $OUTPUT but no"
                             "output_string provided")

    def _translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # interpolate the file names if needed
        if self.output_string is not None:
            command = command.replace("$OUTPUT", self.output_string)
        if self.input_string is not None:
            command = command.replace("$INPUT", self.input_string)

        flags_str = ""
        if self.flags is not None:
            for flag in self.flags:
                flags_str += flag+" "
        flags_str = flags_str[:-1]
        command = command.replace("$FLAGS", flags_str)

        options_str = ""
        if self.options is not None:
            for key, value in sorted(self.options.items()):
                options_str += key+" "+value+" "
        options_str = options_str[:-1]
        command = command.replace("$OPTIONS", options_str)
        return(command)

    def prepare(self):
        '''
            Makes a directory and then moves the input data file there
        '''
        raise NotImplementedError

    def run_cmd(self):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        raise NotImplementedError

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the temp dir
        '''
        raise NotImplementedError
