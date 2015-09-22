import sys, os
import shlex

import xml.etree.ElementTree as ET


os.remove(__file__)


from . import enablegalaxy


CURRENT_PACKAGE_DIR = os.path.dirname(__file__)
INTERPRETER_EXECUTABLE = sys.executable


def configure (args, config):
    prepare_package_files()
    if not 'tmpfiles_path' in args:
        choice = input(
            'Which folder should MiModD use to store temporary data? [{0}]:'
            .format(config.tmpfiles_path))
        if choice:
            args['tmpfiles_path'] = choice
    if not 'snpeff_path' in args:
        choice = input(
            'In which folder should MiModD look for SnpEff? [{0}]:'
            .format(config.snpeff_path))
        if choice:
            args['snpeff_path'] = choice
    if not 'multithreading_level' in args:
        choice = input(
            'Up to how many threads do you want to allow MiModD to use at a time? [{0}]:'
            .format(config.multithreading_level))
        if choice:
            args['multithreading_level'] = choice
    if not 'max_memory' in args:
        choice = input(
            'Up to how much memory in GB do you want to allow MiModD to use? [{0}]:'
            .format(config.max_memory))
        if choice:
            args['max_memory'] = choice
    print("""
All necessary information has been collected. Hit <Enter> to store your settings and start using MiModD.

To change settings later, you can rerun this tool with new settings provided as command line options.

""")
    _ = input()


def prepare_package_files ():
    fix_executable_shebang()
    prepare_galaxy_integration()


def fix_executable_shebang ():
    scripts_dir = os.path.join(CURRENT_PACKAGE_DIR, 'bin')
    # Adjust the shebang line to the environment if possible.
    if INTERPRETER_EXECUTABLE and not ' ' in INTERPRETER_EXECUTABLE:
        # with POSIX systems there is no way to form a valid shebang line
        # if there is a space in the executable path so we leave the file alone.
        # Under Windows we could do:
        # if ' ' in interpreter_executable:
        #    # quote the interpreter path if it contains spaces
        #    interpreter_executable = '"%s"' % interpreter_executable

        with open(os.path.join(scripts_dir, 'mimodd'), 'r') as script_in:
            first_line = script_in.readline()
            if not first_line.startswith('#!'):
                raise RuntimeError(
                    'Compromised starter script.'
                    )
            first_line = '#!' + INTERPRETER_EXECUTABLE + '\n'
            remaining_lines = script_in.readlines()
        with open(os.path.join(scripts_dir, 'mimodd'), 'w') as script_out:
            script_out.write(first_line)
            script_out.writelines(remaining_lines)


def prepare_galaxy_integration ():
    tool_wrapper_dir = os.path.join(CURRENT_PACKAGE_DIR,
                                    'galaxy_data',
                                    'mimodd')
    enablegalaxy.GalaxyAccess.set_toolbox_path()
    if INTERPRETER_EXECUTABLE:
        interpreter_executable = shlex.quote(INTERPRETER_EXECUTABLE)
        mimodd_command = '{0} -m MiModD'.format(interpreter_executable)
        for wrapper in os.listdir(tool_wrapper_dir):
            try:
                wrapper_tree = ET.parse(os.path.join(tool_wrapper_dir, wrapper))
            except ET.ParseError:
                galaxy_integration_warn(tool_wrapper_dir, wrapper)
                continue
            wrapper_root = wrapper_tree.getroot()
            if not wrapper_root.tag == 'tool':
                galaxy_integration_warn(tool_wrapper_dir, wrapper)
                continue
            else:
                wrapper_version_element = wrapper_root.find('version_command')
                wrapper_version_element.text = \
                    wrapper_version_element.text.replace('mimodd',
                                                         mimodd_command)
                wrapper_command_element = wrapper_root.find('command')
                wrapper_command_element.text = \
                    wrapper_command_element.text.replace('mimodd',
                                                         mimodd_command)
                wrapper_tree.write(os.path.join(tool_wrapper_dir, wrapper))

                
def galaxy_integration_warn(tool_wrapper_dir, wrapper):
    print('Galaxy Integration Warning: File {0} in Galaxy tool wrapper directory {1} cannot be parsed as a wrapper xml.'
          .format(wrapper, tool_wrapper_dir))
