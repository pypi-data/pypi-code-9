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

'''
    Insert FB SDK into PYTHONPATH
'''

import sys
import os

this_dir = os.path.dirname(__file__)
repo_dir = os.path.join(this_dir, os.pardir, os.pardir)
sys.path.insert(1, repo_dir)

from facebookads import bootstrap
bootstrap.auth()


'''
    This script executes an example from FB Python Ads SDK and prints only
    exceptions thrown while using it. If nothing is thrown, output is supressed.
    Different error codes expose the exception returned.
'''

import StringIO
import contextlib

from facebookads.exceptions import FacebookError


def usage():
    usage = 'Usage: \n\tpython docs_runner.py ' \
            '<PATH_TO_EXAMPLE_FILE_1> [<PATH_TO_EXAMPLE_FILE_2>, ...]\n'
    print(usage)
    sys.exit(1)


@contextlib.contextmanager
def ignore_stdout(stdout=None):
    '''
        Redirects stdout output from scripts being executed. Usage:
        with ignore_stdout() as s:
            script_with_supressed_output()
            print(s.getvalue())
    '''
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    with ignore_stdout() as ignored_output:
        for file_to_run in sys.argv[1:]:
            print(file_to_run)
            try:
                execfile(file_to_run)
            except FacebookError as err:
                print(
                    'Exception thrown in {}'.format(file_to_run),
                    file=sys.stderr,
                )
                print(err, file=sys.stderr)
                sys.exit(1)
            except SyntaxError as err:
                print(err, file=sys.stderr)
                sys.exit(1)
            except Exception as err:
                print(err, file=sys.stderr)
                sys.exit(1)
