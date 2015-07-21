# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define API Topics."""

import base64
import datetime

import pytz

from gcloud._helpers import _RFC3339_MICROS


class Message(object):
    """Messages can be published to a topic and received by subscribers.

    See:
    https://cloud.google.com/pubsub/reference/rest/google/pubsub/v1beta2/PubsubMessage

    :type data: bytes
    :param data: the payload of the message

    :type message_id: string
    :param message_id: An ID assigned to the message by the API.

    :type attributes: dict or None
    :param attributes: Extra metadata associated by the publisher with the
                       message.
    """
    def __init__(self, data, message_id, attributes=None):
        self.data = data
        self.message_id = message_id
        self._attributes = attributes

    @property
    def attributes(self):
        """Lazily-constructed attribute dictionary"""
        if self._attributes is None:
            self._attributes = {}
        return self._attributes

    @property
    def timestamp(self):
        """Return sortable timestamp from attributes, if passed.

        Allows sorting messages in publication order (assuming consistent
        clocks across all publishers).

        :rtype: datetime
        :returns: timestamp (in UTC timezone) parsed from RFC 3339 timestamp
        :raises: ValueError if timestamp not in ``attributes``, or if it does
                 not match the RFC 3339 format.
        """
        stamp = self.attributes.get('timestamp')
        if stamp is None:
            raise ValueError('No timestamp')
        return datetime.datetime.strptime(stamp, _RFC3339_MICROS).replace(
            tzinfo=pytz.UTC)

    @classmethod
    def from_api_repr(cls, api_repr):
        """Factory:  construct message from API representation.

        :type api_repr: dict or None
        :param api_repr: The API representation of the message
        """
        data = base64.b64decode(api_repr['data'])
        return cls(data=data, message_id=api_repr['messageId'],
                   attributes=api_repr.get('attributes'))
