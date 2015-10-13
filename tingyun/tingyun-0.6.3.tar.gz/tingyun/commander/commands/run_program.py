from __future__ import print_function

import os
import sys
from tingyun.logistics.exceptions import CommandlineParametersException
from tingyun.config.start_log import log_message
from tingyun import __file__ as root_dir


class Command(object):
    """
    """
    def __init__(self):
        """
        """
        self.name = "run-program"  # order format with commandline
        self.options = 'command [parameters]'
        self.description = "Executes the command with parameters."

    def execute(self, args):
        """
        :param args:
        :return:
        """
        if 0 == len(args):
            raise CommandlineParametersException()

        log_message('-------------get in bootstrap--------------')
        log_message('TingYun Admin Script (%s)', __file__)
        log_message('working_directory = %r', os.getcwd())
        log_message('current_command = %r', sys.argv)
        log_message('sys.prefix = %r', os.path.normpath(sys.prefix))

        log_message('sys.executable = %r', sys.executable)
        log_message('sys.flags = %r', sys.flags)
        log_message('sys.path = %r', sys.path)

        boot_directory = os.path.join(os.path.dirname(root_dir), 'flashpoint')
        log_message('boot_directory = %r', boot_directory)

        # before change the pythonpath. we should load the exist, then add myself into
        final_python_path = boot_directory
        if 'PYTHONPATH' in os.environ:
            path = os.environ['PYTHONPATH'].split(os.path.pathsep)
            if boot_directory not in path:
                final_python_path = "%s%s%s" % (boot_directory, os.path.pathsep, os.environ['PYTHONPATH'])

        log_message('python_path = %r', final_python_path)
        os.environ['PYTHONPATH'] = final_python_path

        # deal the program exe as a system command, and change to full system path
        program_exe_path = args[0]
        if not os.path.dirname(program_exe_path):
            program_target_path = os.environ.get('PATH', '').split(os.path.pathsep)
            log_message("get the path from env:%s", program_target_path)
            for path in program_target_path:
                program_exe_path_tmp = os.path.join(path, program_exe_path)
                if os.path.exists(program_exe_path_tmp) and os.access(program_exe_path_tmp, os.X_OK):
                    program_exe_path = program_exe_path_tmp
                    log_message("match the program exe: %s", program_exe_path)
                    break

        log_message('program_exe_path = %r', program_exe_path)
        log_message('execl_arguments = %r', [program_exe_path] + args)

        os.execl(program_exe_path, *args)
