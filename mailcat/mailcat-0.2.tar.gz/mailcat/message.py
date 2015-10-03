# Copyright (C) 2015  Andrey Golovizin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sys import version_info

import email
from email.header import make_header, decode_header


if version_info.major == 3 and version_info.minor >= 4 or version_info.major > 3:
    from email.message import EmailMessage
else:
    from ._backports import EmailMessage


if version_info.major >= 3:
    unicode = str
    message_from_binary_file = email.message_from_binary_file
else:
    message_from_binary_file = email.message_from_file


class UnicodeEmailMessage(EmailMessage):
    def get_payload_text(self):
        payload = self.get_payload(decode=True)
        if payload is not None:
            return payload.decode(self.get_content_charset('latin1'), 'replace').strip()
        else:
            return ''

    def get_unicode_header(self, name, failobj=None):
        value = self.get(name, failobj)
        if value is None:
            return failobj
        header = make_header(decode_header(value))
        try:
            return unicode(header)
        except UnicodeDecodeError:
            # incorrectly formatted message
            return value.decode('latin1', 'replace')

        try:
            return self[name]
        except KeyError:
            return failobj

    @classmethod
    def fromfile(cls, file):
        return message_from_binary_file(file, _class=cls)
