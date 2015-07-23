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
import sys

from command import Command, MirrorSafeCommand
from git_command import git
from git_refs import HEAD


class Version(Command, MirrorSafeCommand):
    wrapper_version = None
    wrapper_path = None

    common = False
    helpSummary = "Display the version of andromeda"
    helpUsage = """
%prog
"""

    def Execute(self, opt, args):
        rp = self.manifest.repoProject
        rem = rp.GetRemote(rp.remote.name)

        print('andromeda version %s' % rp.work_git.describe(HEAD))
        print('       (from %s)' % rem.url)

        if Version.wrapper_path is not None:
            print('andromeda launcher version %s' % Version.wrapper_version)
            print('       (from %s)' % Version.wrapper_path)

        print(git.version().strip())
        print('Python %s' % sys.version)
