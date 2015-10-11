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

from cryptography import fernet
import msgpack
import six


def _restore_padding(token):
    """Restore padding based on token size.

    :param token: token to restore padding on
    :returns: token with correct padding

    """
    # Re-inflate the padding
    mod_returned = len(token) % 4
    if mod_returned:
        missing_padding = 4 - mod_returned
        token += b'=' * missing_padding
    return token


def unpack_token(fernet_token, fernet_keys):
    """Attempt to unpack a token using the supplied Fernet keys.

    :param fernet_token: token to unpack
    :type fernet_token: string
    :param fernet_token: a list consisting of keys in the repository
    :type fernet_token: string
    :returns: the token payload
    :raises: Exception in the event the token can't be unpacked

    """
    # create a list of fernet instances
    fernet_instances = [fernet.Fernet(key) for key in fernet_keys]
    # create a encryption/decryption object from the fernet keys
    crypt = fernet.MultiFernet(fernet_instances)

    # attempt to decode the token
    token = _restore_padding(six.binary_type(fernet_token))
    serialized_payload = crypt.decrypt(token)
    payload = msgpack.unpackb(serialized_payload)

    translated_payload = []
    for item in payload:
        if isinstance(item, list):
            translated_item = []
            for i in item:
                translated_item.append(i)
            translated_payload.append(translated_item)
        else:
            translated_payload.append(item)

    # present token values
    return translated_payload
