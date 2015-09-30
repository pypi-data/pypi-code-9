from __future__ import print_function

import cmd
import sys
import traceback
import string
import textwrap

from docopt import docopt
import cloudmesh_cmd3light.plugins

from cloudmesh_cmd3light.plugins.Bar import BarCommand


from cloudmesh_cmd3light.version import version
from cloudmesh_base.util import get_python
from cloudmesh_base.util import check_python
import cloudmesh_base
from cloudmesh_base.tables import dict_printer
from cloudmesh_cmd3light.command import command, Cmd3Command
import imp

class CloudmeshContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

import importlib

names  = [cls.__name__ for cls in Cmd3Command.__subclasses__()]
classes  = [cls for cls in Cmd3Command.__subclasses__()]


# type(cmd.Cmd)("MyCli", bases + (cmd.Cmd,), {})
# noinspection PyPep8Naming
class CloudmeshBaseConsole(cmd.Cmd,
                       cloudmesh_cmd3light.plugins.CommandsCommands,
                       cloudmesh_cmd3light.plugins.TerminalCommands,
                       cloudmesh_cmd3light.plugins.ManCommand,
                       cloudmesh_cmd3light.plugins.SecureShellCommand,
                       cloudmesh_cmd3light.plugins.OpenCommand):
    """
    Cloudmesh Console
    """

    stdout = sys.stdout
    command_topics = {}

    def register_topics(self):
        topics = {}
        for command in self.default_plugins:
            tmp = command.topics.copy()
            topics.update(tmp)
        for name in topics:
            self.register_command_topic(topics[name], name)
        for name in ["q", "EOF", "man"]:
            self.register_command_topic("shell", name)


    def __init__(self, context, plugins=None):
        self.default_plugins = \
            [cls for cls in Cmd3Command.__subclasses__()]

        self.default_plugin_names = \
            [cls.__name__ for cls in Cmd3Command.__subclasses__()]

        cmd.Cmd.__init__(self)
        self.command_topics = {}
        self.register_topics()
        self.context = context

        if self.context.debug:
            print("init CloudmeshConsole")

        self.prompt = 'cm> '

        self.banner = textwrap.dedent("""
            +=======================================================+
            .   ____ _                 _                     _      .
            .  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   .
            . | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  .
            . | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | .
            .  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| .
            +=======================================================+
                                 Cloudmesh Shell
            """)
        # KeyCommands.__init__(self, context)
        for c in CloudmeshConsole.__bases__[1:]:
            c.__init__(self, context)

    def preloop(self):
        """adds the banner to the preloop"""

        if self.context.splash:
            lines = textwrap.dedent(self.banner).split("\n")
            for line in lines:
                # Console._print("BLUE", "", line)
                print(line)

    def do_EOF(self, args):
        """
        ::

            Usage:
                EOF

            Description:
                Command to the shell to terminate reading a script.
        """
        return True

    def do_quit(self, args):
        """
        ::

            Usage:
                quit

            Description:
                Action to be performed whne quit is typed
        """
        return True

    do_q = do_quit

    def emptyline(self):
        return

    def do_context(self, args):
        """
        ::

            Usage:
                context

            Description:
                Lists the context variables and their values
        """
        """
        :param args:
        :return:
        """
        print(self.context.__dict__)

    @command
    def do_version(self, args, arguments):
        """
        Usage:
           version [--format=FORMAT] [--check=CHECK]

        Options:
            --format=FORMAT  the format to print the versions in [default: table]
            --check=CHECK    boolean tp conduct an additional check [default: True]

        Description:
            Prints out the version number
        """

        python_version, pip_version = get_python()

        versions = {
            "cloudmesh_base": {
                "name": "cloudmesh_base",
                "version": str(cloudmesh_base.version)
            },
            "python": {
                "name": "python",
                "version": str(python_version)
            },
            "pip": {
                "name": "pip",
                "version": str(pip_version)
            }
        }

        print (dict_printer(versions, output=arguments["--format"] ,order=["name", "version"]))
        if arguments["--check"] in ["True"]:
            check_python()

    def register_command_topic(self, topic, command_name):
        try:
            a = self.command_topics[topic]
        except:
            self.command_topics[topic] = []
        self.command_topics[topic].append(command_name)

    def do_help(self, arg):
        """
        ::

            Usage:
                help
                help COMMAND

            Description:
                List available commands with "help" or detailed help with
                "help COMMAND"."""

        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help_page = {}
            for name in names:
                if name[:5] == 'help_':
                    help_page[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in help_page:
                        cmds_doc.append(cmd)
                        del help_page[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)

            self.stdout.write("%s\n" % str(self.doc_leader))
            self.print_topics(self.doc_header, cmds_doc, 15, 80)
            self.print_topics(self.misc_header, list(help_page.keys()), 15, 80)
            self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

            for topic in self.command_topics:
                topic_cmds = sorted(self.command_topics[topic], key=str.lower)
                self.print_topics(string.capwords(topic + " commands"), topic_cmds, 15, 80)

    def help_help(self):
        """
        ::

            Usage:
               help NAME

            Prints out the help message for a given function
        """
        print (textwrap.dedent(self.help_help.__doc__))
    '''
    @command
    def do_bar(self, arg, arguments):
        """Usage:
                bar -f FILE
                bar FILE
                bar list

        This command does some useful things.

        Arguments:
              FILE   a file name

        Options:
              -f      specify the file

        """
        print(arguments)
    '''

# MyClass = type('MyClass', (), {})

def get_class(str):
    getattr(sys.modules[__name__], str)

def cmd3_factory(bases=None):
    # classes  = [cls for cls in Cmd3Command.__subclasses__()]
    #    included_bases = [cls for cls in CloudmeshBaseConsole.__subclasses__()]

    console_base = (CloudmeshBaseConsole,)

    if bases is not None:
        new_bases =  ()
        for base in bases:
            new_bases += (base,)
        bases = new_bases + console_base
    else:
        bases = console_base
    return type("CloudmeshConsole", bases, {})


CloudmeshConsole =  cmd3_factory(
   [cloudmesh_cmd3light.plugins.Bar.BarCommand]
)
# CloudmeshConsole =  cmd3_factory()


def simple():
    context = CloudmeshContext(debug=True,
                               splash=True)
    con = CloudmeshConsole(context)
    con.cmdloop()


def main():
    """cm.

    Usage:
      cm --help
      cm [--debug] [--nosplash] [--file=SCRIPT] [-i] [COMMAND ...]

    Arguments:
      COMMAND                  A command to be executed

    Options:
      --file=SCRIPT  -f  SCRIPT  Executes the script
      -i                 After start keep the shell interactive,
                         otherwise quit [default: False]
      --nosplash    do not show the banner [default: False]
    """

    try:
        arg = docopt(main.__doc__, help=True)
        if arg['--help']:
            print(main.__doc__)
            sys.exit()

        # fixing the help parameter parsing

        #   arguments['COMMAND'] = ['help']
        #   arguments['help'] = 'False'

        script_file = arg['--file']

    except:
        script_file = None
        interactive = False

        arguments = sys.argv[1:]
        arg = {
            '--debug': '--debug' in arguments,
            '--nosplash': '--nosplash' in arguments,
            '-i': '-i' in arguments}

        for a in arg:
            if arg[a]:
                arguments.remove(a)

        arg['COMMAND'] = [' '.join(arguments)]

    splash = not arg['--nosplash']
    debug = arg['--debug']
    interactive = arg['-i']


    context = CloudmeshContext(debug=debug,
                               splash=splash)
    cmd = CloudmeshConsole(context)


    if len(arg['COMMAND']) > 0:
        try:
            user_cmd = " ".join(arg['COMMAND'])
            if debug:
                print(">", user_cmd)
            cmd.onecmd(user_cmd)
        except Exception, e:
            print("ERROR: executing command '{0}'".format(user_cmd))
            print(70 * "=")
            print(e)
            print(70 * "=")
            print(traceback.format_exc())

        if interactive:
            cmd.cmdloop()

    elif not script_file or interactive:
        cmd.cmdloop()


if __name__ == "__main__":
    main()

    # simple()
