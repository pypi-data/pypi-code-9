#
# Copyright (C) 2009 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Original code can be found here: https://android.googlesource.com/tools/repo/
# This is a refactor for the OpenStack project with an upgrade to Python 3.
# All code changes will be marked.
# Formatting changed to meet PEP8 requirements.

from __future__ import print_function
from optparse import SUPPRESS_HELP
import sys

from command import Command, MirrorSafeCommand
from subcmds.sync import _PostRepoUpgrade
from subcmds.sync import _PostRepoFetch


class Selfupdate(Command, MirrorSafeCommand):
    common = False
    helpSummary = "Update andromeda to the latest version"
    helpUsage = """
%prog
"""
    helpDescription = """
The '%prog' command upgrades andromeda to the latest version, if a
newer version is available.

Normally this is done automatically by 'andromeda sync' and does not
need to be performed by an end-user.
"""
    #TODO verify if these can be refactored.
    def _Options(self, p):
        g = p.add_option_group('andromeda version options')
        g.add_option('--no-repo-verify',
                     dest='no_repo_verify', action='store_true',
                     help='Do not verify andromeda source code. NOT RECOMMENDED.')
        g.add_option('--repo-upgraded',
                     dest='repo_upgraded', action='store_true',
                     help=SUPPRESS_HELP)

    def Execute(self, opt, args):
        rp = self.manifest.repoProject
        rp.PreSync()

        if opt.repo_upgraded:
            _PostRepoUpgrade(self.manifest)

        else:
            if not rp.Sync_NetworkHalf():
                print("error: can't update andromeda", file=sys.stderr)
                sys.exit(1)

            rp.bare_git.gc('--auto')
            _PostRepoFetch(rp,
                           no_repo_verify=opt.no_repo_verify,
                           verbose=True)
