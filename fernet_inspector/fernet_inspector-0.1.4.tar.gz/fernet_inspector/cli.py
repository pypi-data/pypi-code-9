# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os

import fernet_inspector


def _get_args():
    """Get arguments from the user."""
    parser = argparse.ArgumentParser(
        prog='fernet-inspector',
        description='Inspect the contents of a Keystone Fernet token from '
                    'the host it was issued from.')
    parser.add_argument('token', type=str, help='token to decrypt')
    parser.add_argument('-k', '--key-repository', type=str,
                        default='/etc/keystone/fernet-keys/',
                        help='location of Fernet key repository.')
    args = parser.parse_args()
    return args.token, args.key_repository


def _read_keys_from_disk(key_repository):
    """Read the keys from the key repository."""
    # validate the repository location
    if not os.path.isdir(key_repository):
        raise fernet_inspector.NonExistentKeyRepository()

    # build a dictionary of key_number:encryption_key pairs
    keys = dict()
    for filename in os.listdir(key_repository):
        path = os.path.join(key_repository, str(filename))
        if os.path.isfile(path):
            with open(path, 'r') as key_file:
                try:
                    key_id = int(filename)
                except ValueError:
                    pass
                else:
                    keys[key_id] = key_file.read()

    # return a list of key values
    return [keys[x] for x in sorted(keys.keys(), reverse=True)]


def main():
    """The main entry point into the fernet_inspector."""
    # get arguments
    fernet_token, key_repository = _get_args()

    # build key set
    fernet_keys = _read_keys_from_disk(key_repository)

    # pass required stuff to the inspector and print the result
    print fernet_inspector.unpack_token(fernet_token, fernet_keys)
