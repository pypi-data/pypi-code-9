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

if version_info.major >= 3 and version_info.major > 2:
    from email.parser import BytesFeedParser
else:
    from email.parser import FeedParser as BytesFeedParser


from .message import UnicodeEmailMessage


def is_mbox_header(line):
    return len(line) >= 5 and line[:5] == b'From '


def iter_messages(file):
    for line in file:
        if not line:
            continue
        if is_mbox_header(line):
            for message in iter_mbox_messages(file): yield message
        else:
            parser = BytesFeedParser(_factory=UnicodeEmailMessage)
            parser.feed(line)
            for line in file:
                parser.feed(line)
            message = parser.close()
            if message.keys():  # if no headers, probably not a MIME message
                yield message


def iter_mbox_messages(file):
    has_more = True
    while has_more:
        message, has_more = read_mbox_message(file)
        yield message


def read_mbox_message(file):
    parser = BytesFeedParser(_factory=UnicodeEmailMessage)

    for line in file:
        if is_mbox_header(line):
            return parser.close(), True
        else:
            parser.feed(line)
    return parser.close(), False
