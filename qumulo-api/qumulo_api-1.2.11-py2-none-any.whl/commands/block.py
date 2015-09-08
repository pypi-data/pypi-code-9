# Copyright (c) 2015 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.block as block

class GetBlockSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = "block_settings_get"
    DESCRIPTION = "Return block settings for a node."

    @staticmethod
    def main(conninfo, credentials, _args):
        print block.get_block_settings(conninfo, credentials)

class SetBlockSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = "block_settings_set"
    DESCRIPTION = "Set block settings for a node."

    @staticmethod
    def options(parser):
        parser.add_argument("--expiration-pct", help="Expiration "
               "percentage value.", required=True, type=int)

    @staticmethod
    def main(conninfo, credentials, args):
        print block.set_block_settings(conninfo, credentials,
                args.expiration_pct)
