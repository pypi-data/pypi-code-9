 # This file is part of widediaper.

# widediaper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# widediaper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with widediaper.  If not, see <http://www.gnu.org/licenses/>

from __future__ import print_function

import sys
import re
from os.path import join as path_join

import pandas as pd

from pexpect.replwrap import REPLWrapper

from widediaper.parse.check_command import check_command
from widediaper.parse.output import remove_repl_output_prefix, return_correct_type
from widediaper.r_session.log_session import write_to_file_and_stream
from widediaper.r_session.session_helpers import get_outfolder, get_df_path

from ebs.version import PY3

class R(object):


    def __init__(self, outstream=False, session_folder="", exit_on_error=True):

        self.session = REPLWrapper("R", u">", "options(prompt='<<|>>')",
                                   new_prompt=u'<<|>>')

        self.outstream = outstream
        self.exit_on_error = exit_on_error

        session_pid = remove_repl_output_prefix(
            self.session.run_command("Sys.getpid()"))
        self.session_folder = get_outfolder(session_folder, session_pid)

        self.outfile = path_join(self.session_folder, "widediaper.R")


    def __call__(self, command, timeout=None):
        """Calls a command with the current R session.

        Note that it first
        1) writes the command to the desired outputstream,
        2) parses the command to see if it contains an unmatched
           parenthesis or quote which would make R hang,
        3) then calls the command,
        4) lastly it parses the output (i.e. removes repl noise) and
        5) returns the result."""

        write_to_file_and_stream(command, self.outstream, self.outfile)

        check_command(command)

        result_repl = self.session.run_command(command, timeout=timeout)

        result = remove_repl_output_prefix(result_repl)

        if re.search("error", result, re.IGNORECASE):
            print("Error returned by R call:\n", result, file=sys.stderr)

            if self.exit_on_error:
                sys.exit(1)

        result_correct_type = return_correct_type(result)

        return result_correct_type


    def send(self, df, name):

        df_path = get_df_path(self.session_folder, "to_r", name)

        df.to_csv(df_path, sep="\t")
        get = "{name} = read.delim('{df_path}', row.names=1)" \
            .format(name=name, df_path=df_path)

        self(get)


    def get(self, name):
        df_path = get_df_path(self.session_folder, "from_r", name)
        write_command = "write.table({name}, '{df_path}', sep='\\t', quote=F, na='NA')"\
            .format(**vars())
        self(write_command)

        return pd.read_table(df_path, sep="\t", header=0, index_col=0)


    def load_library(self, library):

        try:
            r_msg = self("library('{}')".format(library))

            if u"error" in r_msg or u"Error" in r_msg:

                if PY3:
                    raise ImportError(r_msg)
                else:
                    raise ImportError(r_msg.encode('ascii', 'ignore'))


        except ImportError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
