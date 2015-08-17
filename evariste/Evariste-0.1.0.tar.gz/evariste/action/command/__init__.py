# Copyright Louis Paternault 2015
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Shell command: perform a (list of) shell command(s) on files."""

import logging
import os
import pathlib
import re
import shutil
import shlex
import subprocess
import tempfile
import threading

from evariste import errors
from evariste.action import Action, PathCompiler, Report
from evariste.action import LogPipe, MultiLog
from evariste.hooks import MethodHook
import evariste

LOGGER = logging.getLogger(evariste.__name__)
STRACE_RE = re.compile(r'^\d* *open\("(?P<name>.*)",.*O_RDONLY.*\) = *[^ -].*')

class MissingOption(errors.EvaristeError):
    """No command was provided for action :class:`Command`."""

    def __init__(self, filename, section, option):
        super().__init__()
        self.filename = filename
        self.section = section
        self.option = option

    def __str__(self):
        return (
            "Configuration for file '{file}' is missing option '{option}' in section '{section}'."
            ).format(
                file=self.filename,
                section=self.section,
                option=self.option,
            )

def system(command, path, logreaders, depends, tempdir):
    """Run a system command.

    This function:
    - run command;
    - log standard output and error;
    - track opened files.
    """

    def _process_strace_line(line):
        """Process output line of strace, and complete ``depends`` if relevant."""
        match = STRACE_RE.match(line)
        if match:
            name = pathlib.Path(path.parent.from_fs) / pathlib.Path(match.groupdict()["name"])
            if name != path.from_fs:
                if path.vcs.is_versionned(name):
                    depends.add(name)

    def _process_strace(pipe):
        """Process strace output, to find dependencies."""
        with open(pipe, mode="r", errors="replace") as file:
            for line in file:
                _process_strace_line(line)

    stdout = list(os.pipe())
    stderr = list(os.pipe())
    fifo = os.path.join(tempdir, str(id(path)))
    os.mkfifo(fifo)

    process = subprocess.Popen(
        r"""strace -f -o "{dest}" -e trace=open sh -c {command}""".format(
            dest=fifo,
            command=shlex.quote(command),
            ),
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=stdout[1],
        stderr=stderr[1],
        pass_fds=stdout + stderr,
        universal_newlines=True,
        cwd=path.parent.from_fs.as_posix(),
        )

    threads = [
        threading.Thread(
            target=function,
            daemon=True,
            kwargs={
                'pipe' : pipe,
                }
            )
        for (function, pipe) in [
            (_process_strace, fifo),
            (logreaders[0], stdout[0]),
            (logreaders[1], stderr[0]),
            ]
        ]
    for thread in threads:
        thread.start()
    process.wait()
    for pipe in stdout, stderr:
        os.close(pipe[1])
    os.unlink(fifo)
    for thread in threads:
        thread.join()

    return process.returncode

class CommandCompiler(PathCompiler):
    """Run commands on the path."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._commands = []
        self._report = None # Temporary report. It will be completed during compilation.

    def iter_commands(self):
        """Iterator over the list of commands."""
        yield from self._commands

    @property
    def tempdir(self):
        """Return the path of a temporary, as secure as possible, directory."""
        return self.parent.tempdir

    def run_subcommand(self, command):
        """Run the subcommand ``command``."""
        LOGGER.info("Running command: {}".format(command))
        pipes = [
            LogPipe(1),
            LogPipe(2),
            ]
        self._report.log.append(MultiLog(pipes))

        with self.shared.builder.lock.thread_safe():
            returncode = system(
                command=command,
                path=self._report.path,
                logreaders=[log.read for log in pipes],
                depends=self._report.depends,
                tempdir=self.tempdir,
                )
        return returncode == 0

    def _read_config(self):
        """Read and parse list of commands from configuration file."""
        self._commands = []
        for option in self.path.config[self.plugin_id]:
            if option.startswith("command"):
                self._commands.append(
                    self.path.format(
                        self.path.config[self.plugin_id][option]
                        )
                    )
        if not self._commands:
            raise MissingOption(self.path.from_fs, self.plugin_id, 'command*')
        if not self.path.config[self.plugin_id]['target'] is not None:
            raise MissingOption(self.path.from_fs, self.plugin_id, 'target')
        self._report.target = (
            self.path.parent.from_source.as_posix()
            /
            pathlib.Path(self.path.format(self.path.config[self.plugin_id]["target"]))
            )


    def compile(self):
        """Perform compilation of `self.path`."""
        self._report = Report(
            self.path,
            success=True,
            )
        self._read_config()
        for command in self.iter_commands():
            parsed_command = self.path.format(command)
            if not self.run_subcommand(parsed_command):
                self._report.success = False
                self._report.error = "Command '{}' failed.".format(parsed_command)
                break
        return self._report

class TempDir(MethodHook):
    """Manage creation and deletion of a temporary directory."""

    def pre(self, *__args, **__kwargs):
        self.plugin.tempdir = tempfile.mkdtemp(
            prefix="evariste-{}-{}-".format(os.getpid(), self.plugin.plugin_id),
            )

    def post(self, value):
        shutil.rmtree(self.plugin.tempdir)
        return value

class Command(Action):
    """Chain of commands"""

    keyword = "command"
    pathcompiler = CommandCompiler
    hooks = {
        'compiletree': TempDir,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tempdir = None

    def match(self, value):
        return False

