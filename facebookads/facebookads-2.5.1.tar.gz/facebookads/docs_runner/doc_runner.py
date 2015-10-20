# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import print_function
from __future__ import unicode_literals

import sys
import os

import traceback
import contextlib
import argparse

description = '''
    This script executes an example from FB Python Ads SDK and prints only
    exceptions thrown while using it. If nothing is thrown, output is supressed.
'''

# Use facebookads SDK from this repo instead of the one installed via pip
this_dir = os.path.dirname(__file__)
repo_dir = os.path.join(this_dir, os.pardir, os.pardir)
sys.path.insert(1, repo_dir)

from facebookads.api import FacebookAdsApi
from facebookads.exceptions import FacebookError
from facebookads import test_config

access_token = test_config.access_token
app_id = test_config.app_id
app_secret = test_config.app_secret

FacebookAdsApi.init(app_id, app_secret, access_token)

@contextlib.contextmanager
def redirect_stdout(stdout=None):
    '''
        Redirects stdout output from scripts being executed.
        It defaults to redirecting to /dev/null
        Usage:
        with redirect_stdout() as s:
            script_with_supressed_output()
            print(s.getvalue())
    '''
    old = sys.stdout
    if stdout is None:
        stdout = open(os.devnull, 'w')
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-o',
        '--show-stdout',
        action='store_true',
        help='prints output to stdout instead of supressing it'
    )
    parser.add_argument(
        'docsmith_file',
        nargs='+',
        help='docsmith example to be tested'
    )
    args = parser.parse_args()

    output_destination = open(os.devnull, 'w')
    if args.show_stdout:
        output_destination = sys.stdout

    files_to_run = args.docsmith_file

    exit_code = 0

    with redirect_stdout(output_destination):
        for file_to_run in files_to_run:
            print('Executing file', file_to_run, file=sys.stderr)
            try:
                code_string = open(file_to_run).read()
                code = compile(code_string, file_to_run, 'exec')
                exec(code)
                print('OK\n', file=sys.stderr)
            except Exception as err:
                exit_code = 1
                print(
                    '{} thrown in {}'.format(
                        err.__class__.__name__, file_to_run),
                    file=sys.stderr,
                )
                print('-' * 60, '\n', file=sys.stderr)
                traceback.print_exc()
                print('-' * 60, '\n', file=sys.stderr)

    exit(exit_code)
