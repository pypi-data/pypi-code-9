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


from .utils import join_iter


def indent_header(name, value, max_len):
    indentation_first = max_len - len(name)
    indentation = max_len + 2
    return ' ' * indentation_first + ('\n' + ' ' * indentation).join(value.splitlines())


class Formatter:
    CORE_HEADERS = 'Subject', 'From', 'To', 'CC', 'Date'
    HEADER_COLOR = 'blue'
    COLORS = {
        'header': {'color': 'blue', 'attrs': ['bold']},
        'quotation': {'color': 'green', 'attrs': ['dark']},
        'attachment': {'color': 'magenta'},
    }

    def __init__(self, msg, all_headers=False, body_type='text', color=False):
        self.msg = msg
        self.all_headers = all_headers
        self.body_type = body_type
        self.color = color

    def highlight(self, text, text_type):
        from termcolor import colored
        return colored(text, **self.COLORS[text_type]) if self.color else text

    @join_iter('\n')
    def highlight_body(self, text):
        for line in text.splitlines():
            yield self.highlight(line, 'quotation') if line.startswith('>') else line

    @join_iter('\n')
    def format_core_headers(self):
        headers = [header for header in self.CORE_HEADERS if header in self.msg]
        max_len = max(len(header) for header in headers) if headers else 0
        for header in headers:
            name = self.highlight(header, 'header')
            value = self.msg.get_unicode_header(header, '<none>')
            indented_value = indent_header(header, value, max_len)
            yield u'{}: {}'.format(name, indented_value)

    @join_iter('\n')
    def format_all_headers(self):
        for header in self.msg.keys():
            name = self.highlight(header, 'header')
            yield u'{}: {}'.format(name, self.msg.get_unicode_header(header))

    def format_headers(self):
        return self.format_all_headers() if self.all_headers else self.format_core_headers()

    def format_body(self):
        if self.body_type == 'text':
            body = self.msg.get_body(('plain', 'html'))
        else:
            body = self.msg.get_body(('html', 'plain'))
        if not body:
            return None
        body_text = body.get_payload_text()
        if body.get_content_subtype() == 'html':
            if self.body_type == 'raw_html':
                return body_text
            else:
                from html2text import html2text
                body_text = html2text(body_text, bodywidth=0)
        return self.highlight_body(body_text)

    @join_iter('\n')
    def format_attachments(self):
        attachments = list(self.msg.iter_attachments())
        if attachments:
            yield self.highlight('Attachments:', 'attachment')
            for i, attachment in enumerate(attachments, 1):
                number = self.highlight('[{}]'.format(i), 'attachment')
                filename = attachment.get_filename()
                mimetype = self.highlight('({})'.format(attachment.get_content_type()), 'attachment')
                yield u'{} {} {}'.format(number, filename, mimetype)

    def format(self):
        parts = [self.format_headers(), self.format_body(), self.format_attachments()]
        return '\n\n'.join(filter(None, parts))
