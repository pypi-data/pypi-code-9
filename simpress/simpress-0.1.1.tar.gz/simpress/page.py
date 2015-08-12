import hashlib
import os
import re
import subprocess
import tempfile
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


class BlockDiagPreprocessor(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        def x(m):
            cmd = m.group(1)
            content = m.group(2)

            def hashnize(content):
                m = hashlib.md5()
                m.update(content)
                return m.hexdigest()

            def publish_img(cmd, src, outfile):
                with tempfile.NamedTemporaryFile() as f:
                    _f = open(f.name,  'w')
                    _f.write(src)
                    _f.close()
                    subprocess.call(
                        '%s --no-transparency -a -f %s -o %s %s' % (
                            cmd, settings.blockdiag_fontpath, outfile, f.name),
                        shell=True)

            filename = '%s.png' % hashnize(content)
            outfile = os.path.join(settings.deploy_dir, 'blockdiag', filename)
            if not os.path.exists(outfile):
                publish_img(cmd, content, outfile)
            return '<p><img src="/blockdiag/%s"></p>' % filename

        reg = re.compile(r'^```(blockdiag|seqdiag)\s*\n(.+?)^(?:```\s*\n)', re.M | re.S)
        contents = re.sub(reg, x, '\n'.join(lines))
        return contents.split('\n')
