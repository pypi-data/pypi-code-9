import re
from collections import namedtuple

import markdown


Page = namedtuple('Page', ('title', 'content'))


def parse_file(filename):
    return Page(
        title=pick_title(read_file(filename)),
        content=render_md(read_file(filename)))


def pick_title(stream):
    return re.sub(r'^# ', '', next(stream))


def render_md(stream):
    return markdown.markdown('\n'.join(stream), extensions=['gfm'])


def read_file(filename):
    with open(filename) as lines:
        for line in lines:
            yield line.rstrip()
