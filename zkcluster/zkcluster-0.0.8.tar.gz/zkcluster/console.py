import re
import cmd
import sys

from .util import compat
from . import exc
from . import client as _client


class ConsoleCmds(cmd.Cmd):
    def __init__(self, console):
        cmd.Cmd.__init__(self)
        self.console = console

    def _tokenize(self, cmd):
        return [
            token for token in
            re.split(r'\s+', cmd)
            if token
        ]

    def __getattr__(self, key):
        if key.startswith("do_"):
            cmd_name = key[3:]
            try:
                cmd = self.console.cmd.commands[cmd_name]
            except KeyError:
                raise AttributeError(key)

            def go(cmd_):
                self.console._invoke_cmd(cmd)
            return go
        else:
            raise AttributeError(key)

    def do_help(self, cmd):
        self.console._handle_response(
            self.console.cmd.help()
        )

    def emptyline(self):
        pass

    def do_EOF(self, cmd):
        self.do_quit(cmd)

    def postcmd(self, stop, line):
        return not self.console.connected


class Console(_client.LocalClient):
    def __init__(self, *arg, **kw):
        super(Console, self).__init__(*arg, **kw)
        self.console = ConsoleCmds(self)
        self.cmd = _CmdInterface()
        self.cmd.commands_from(self)

    def register_cmds_from(self, source):
        self.cmd.commands_from(source)

    def cmd_servicename(self):
        """Return the service name."""
        from . import server
        return server.Servicename().send(self.rpc_service)

    def cmd_quit(self):
        """Quit the console."""

        self.close()

    def on_disconnect(self, unexpected=False, message=None):
        self.output("Connection closed (%s)" % message)
        self.console.connected = False
        sys.exit(-1 if unexpected else 0)

    def _invoke_cmd(self, cmd, args=(), as_grid=False, as_list=False):
        try:
            response = cmd(*args)
        except exc.RPCError as err:
            self.error(err)
        else:
            return self._handle_response(
                response, as_grid=as_grid, as_list=as_list)

    def _handle_response(self, response, as_grid=False, as_list=False):
        err = False

        if response:
            if not as_grid and isinstance(response, list):
                as_list = True

            if not as_grid and not as_list:
                self.output(compat.text_type(response))
                return True

            if as_grid:
                grid = _render_as_grid()

            while response:
                item = response.pop(0)
                if as_grid:
                    grid.append(item)
                else:
                    self.output(compat.text_type(item))

            if as_grid:
                self.output(compat.text_type(grid))

        return not err

    def interact(self):
        self.console.cmdloop()

    def output(self, text, *args):
        self.console.stdout.write(text % args + "\n")

    def error(self, message):
        self.output("Error: %s", message)

    def cmd_help(self):
        """Command help"""
        self.output(
            "\n".join([
                "Command help:",
            ] + self.cmd._help)
        )


class _CmdInterface(object):
    def __init__(self):
        self._help = []
        self.commands = {}

    def commands_from(self, obj):
        # TOOD: make this interact with the console, with the help,
        # etc.
        for key in dir(obj):
            if key.startswith("cmd_"):
                self.add_command(getattr(obj, key))

    def add_command(self, cmd):
        name = cmd.__name__
        assert name.startswith("cmd_")
        self.commands[name[4:]] = cmd
        self._help.insert(0, "%s - %s" % (name[4:], cmd.__doc__))

    def __getattr__(self, name):
        try:
            return self.commands[name]
        except KeyError:
            raise exc.CommandError("no such command '%s'" % name)


class _render_as_grid(object):
    def __init__(self):
        self.grids = []
        self.current_grid = None

    def append(self, record):
        if not self.current_grid:
            self._create_grid(record)
        elif record.keys() != self.current_grid['keys']:
            self._create_grid(record)

        row = tuple(str(record[key]) for key in self.current_grid['keys'])
        self.current_grid['records'].append(row)
        self.current_grid["max_lengths"] = [
            max(current_length, len(item))
            for item, current_length
            in zip(row, self.current_grid["max_lengths"])
        ]

    def _create_grid(self, record):
        self.current_grid = grid = {
            "records": [],
            "keys": record.keys(),
            "max_lengths": [len(key) for key in record.keys()]
        }
        self.grids.append(grid)

    def __str__(self):
        return "\n".join(
            self._render_grid(grid) for grid in self.grids
        )

    def _render_grid(self, grid):
        max_lengths = grid["max_lengths"]

        tmpl = "    ".join(
            "%%%d.%ds" % (len_, len_) for len_ in max_lengths)

        return "\n".join(
            [tmpl % tuple(grid["keys"])] +
            [
                (tmpl % row)
                for row in grid["records"]
            ]
        )

