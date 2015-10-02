# -*- coding: utf-8 -*-
# Copyright (c) 2015, Matt Boyer
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#     IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#     THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#     PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#     CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#     EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#     PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#     PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#     LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#     NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#     SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
BitBucket webhook to trigger a static site build through Jekyll
"""
from __future__ import print_function

import os
import subprocess
import tempfile

from flask import Flask, request


class CmdError(Exception):
    pass


class Runner(object):

    def __init__(self, cmd, workdir=None):
        if workdir:
            self._workdir = workdir
        else:
            self._workdir = os.path.realpath(os.curdir)
        self._executable = cmd

    def run(self, args, env=None):
        '''
        Runs the executable with the arguments given and returns a list of
        lines produced on its standard output.
        '''

        popen_kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }

        if env:
            popen_kwargs['env'] = env

        if self._workdir:
            popen_kwargs['cwd'] = self._workdir

        git_process = subprocess.Popen(
            [self._executable] + args,
            **popen_kwargs
        )

        try:
            out, err = git_process.communicate()
            git_process.wait()
        except Exception as e:
            raise CmdError("Couldn't run '{cmd} {args}':{newline}{ex}".format(
                cmd=self._executable,
                args=' '.join(args),
                newline=os.linesep,
                ex=str(e)
            ))

        if (0 != git_process.returncode) or err:
            if err:
                err = err.decode('utf_8')
            raise CmdError("'{cmd} {args}' failed with:{newline}{err}".format(
                cmd=self._executable,
                args=' '.join(args),
                newline=os.linesep,
                err=err
            ))

        return out.decode('utf_8').splitlines()


class BBRepo(object):

    BITBUCKET_URL = "bitbucket.org"

    def __init__(self):
        self.scm = None
        self.bb_name = None
        self.private = None

    def from_json(self, json_dict):
        try:
            self.scm = json_dict['scm']
            self.bb_name = json_dict['full_name']
            self.private = json_dict['is_private']
        except KeyError:
            raise

        if self.scm not in ('git', 'hg'):
            raise ValueError

    @property
    def url(self):
        if 'git' != self.scm:
            raise ValueError

        return "{fetch_user}@{url}:{repo_name}.git".format(
            fetch_user=self.scm,
            url=BBRepo.BITBUCKET_URL,
            repo_name=self.bb_name
        )


class Push(object):
    def __init__(self):
        self.type = None
        self.destination = None

    def from_json(self, json_dict):
        try:
            self.type = json_dict['new']['type']
            self.destination = json_dict['new']['name']
        except KeyError:
            raise


class WebHook(object):
    def __init__(self, hook_event):
        self.event = hook_event
        if self.event != 'repo:push':
            raise ValueError
        self.repo = BBRepo()
        self.pushes = []

    def from_json(self, json_dict):
        self.repo.from_json(json_dict['repository'])
        for updated_ref in json_dict['push']['changes']:
            new_push = Push()
            new_push.from_json(updated_ref)
            self.pushes.append(new_push)


app = Flask(__name__)
app.debug = True

try:
    PUBLISH_BRANCH = os.environ['PUBLISH_BRANCH']
except:
    PUBLISH_BRANCH = 'master'

try:
    PUBLISH_DEST = os.path.realpath(os.environ['PUBLISH_DEST'])
    if not os.path.isdir(PUBLISH_DEST):
        raise ValueError
except:
    PUBLISH_DEST = '/var/www/'

app.logger.info(
    "Listening for pushes to %s - will build to %s",
    PUBLISH_BRANCH,
    PUBLISH_DEST
)

@app.route('/', methods=['POST'])
def process_hook():
    try:
        event = request.headers['X-Event-Key']
    except KeyError:
        raise
    hook = WebHook(event)
    hook.from_json(request.json)

    for updated_ref in hook.pushes:
        if ('branch' == updated_ref.type and
                PUBLISH_BRANCH == updated_ref.destination):
            with tempfile.TemporaryDirectory() as temp_dir:
                git_runner = Runner('git', temp_dir)
                git_runner.run([
                    'clone', hook.repo.url,
                    '-q',
                    '-b', updated_ref.destination,
                    '.',
                ])
                jekyll_runner = Runner('jekyll', temp_dir)
                jekyll_runner.run([
                    'build',
                    '--source', temp_dir,
                    '--destination', PUBLISH_DEST
                ])
                return "built"
    return "not_built"


if '__main__' == __name__:
    app.run(host='0.0.0.0', port=8000)
