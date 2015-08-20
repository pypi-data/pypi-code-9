from __future__ import print_function
from tingyun.admin.start_log import log_message


def run_program(args):
    import os
    import sys
    from tingyun import __file__ as root_directory

    name = 'run-program'
    options = 'command parameters'
    description = "Executes the command line with parameters[optional]." \
                  "and initialize the agent automatically at startup."

    if 0 == len(args):
        print('tingyun-admin run-program %s' % options)
        sys.exit(1)

    try:
        # for trace the symbol link, especially virtual env
        log_message('sys.real_prefix = %r', sys.real_prefix)
    except AttributeError:
        pass

    log_message('-------------get in bootstrap--------------')
    log_message('TingYun Admin Script (%s)', __file__)
    log_message('working_directory = %r', os.getcwd())
    log_message('current_command = %r', sys.argv)
    log_message('sys.prefix = %r', os.path.normpath(sys.prefix))
    
    log_message('sys.version_info = %r', sys.version_info)
    log_message('sys.executable = %r', sys.executable)
    log_message('sys.flags = %r', sys.flags)
    log_message('sys.path = %r', sys.path)
    for name in sorted(os.environ.keys()):
        if name.startswith('TINGYUN_') or name.startswith('PYTHON'):
            log_message('%s = %r', name, os.environ.get(name))

    root_directory = os.path.dirname(root_directory)
    boot_directory = os.path.join(root_directory, 'bootstrap')
    python_path = boot_directory

    log_message('root_directory = %r', root_directory)
    log_message('boot_directory = %r', boot_directory)

    if 'PYTHONPATH' in os.environ:
        path = os.environ['PYTHONPATH'].split(os.path.pathsep)
        if boot_directory not in path:
            python_path = "%s%s%s" % (boot_directory, os.path.pathsep, os.environ['PYTHONPATH'])

    log_message('python_path = %r', python_path)
    os.environ['PYTHONPATH'] = python_path
    os.environ['TINGYUN_ADMIN_COMMAND'] = repr(sys.argv)
    os.environ['TINGYUN_PYTHON_PREFIX'] = os.path.normpath(sys.prefix)
    os.environ['TINGYUN_PYTHON_VERSION'] = '.'.join(map(str, sys.version_info[:2]))

    # deal the program exe as a system command, and change to full system path

    program_exe_path = args[0]
    if not os.path.dirname(program_exe_path):
        program_search_path = os.environ.get('PATH', '').split(os.path.pathsep)
        log_message("get the path from env:%s", program_search_path)
        for path in program_search_path:
            path = os.path.join(path, program_exe_path)
            if os.path.exists(path) and os.access(path, os.X_OK):
                program_exe_path = path
                log_message("match the program exe: %s", program_exe_path)
                break

    log_message('program_exe_path = %r', program_exe_path)
    log_message('execl_arguments = %r', [program_exe_path] + args)
    
    os.execl(program_exe_path, *args)
