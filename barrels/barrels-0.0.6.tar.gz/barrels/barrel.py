import hashlib
import transforms
import datetime
import collections
import io
import dateutil.parser
import re


BarrelHead = collections.namedtuple('BarrelHead', ['created', 'mime', 'name', 'sha1', 'length'])
BarrelMeta = collections.namedtuple('BarrelMeta', ['heads', 'comments'])

RE_NON_PRINTABLE = re.compile(r'[\n\t\a\r\f]')
import socket
import os.path
import os
import glob


class PBarrel(object):

    def __init__(self, name, size=1):
        self.hostname = socket.gethostname()
        self.rotate_size = int(size*1000*1000)

        self.pathname, self.name  = os.path.split(name)
        if not self.pathname:
            self.pathname = "."

        self.barrel = Barrel(name)

    def new_name(self):
        return "%s/%s.%s.barrel" %(
            self.pathname,
            self.name,
            transforms.sha1(
                self.hostname + datetime.datetime.utcnow().isoformat()
                ).replace("/", "_").replace("+", "-")
            )

    def rotate(self):
        try:
            os.rename(self.barrel.filename, self.new_name())
        except Exception as e:
            pass


    def add(self, name, data, mime=None):
        try:
            statinfo = os.stat(self.barrel.filename)
            if statinfo.st_size > self.rotate_size:
                self.rotate()
        except Exception as e:
            pass
        self.barrel.add(name, data, mime)

    def all_barrel_filenames(self):
        glob_path = "%s/%s.*.barrel" % (self.pathname, self.name)
        files = glob.glob(glob_path)
        files.append(self.barrel.filename)
        return files

    def filter(self, fun=None):
        for n in self.all_barrel_filenames():
            for y in Barrel(n).filter(fun):
                yield y
    @property
    def meta(self):
        result = BarrelMeta(heads=[], comments=[])
        for n in self.all_barrel_filenames():
            m = Barrel(n).meta
            result.heads.extend(m.heads)
            result.comments.extend(m.comments)
        return result


class Barrel(object):
    def __init__(self, filename):

        self.filename = filename
        if not self.filename.endswith(".barrel"):
            self.filename += ".barrel"

    def add(self, name, data, mime=None):
        if not mime:
            mime = "unspecified"

        name = RE_NON_PRINTABLE.sub('',name)[0:131]
        mime = RE_NON_PRINTABLE.sub('',mime)[0:53]

        digest = transforms.sha1(data)
        d = transforms.dumps(data)
        row = u"%s\t%s\t%s\t%s\t%s\t%s\n" %(
            datetime.datetime.utcnow().isoformat(),
            mime,
            name,
            digest,
            len(data),
            d
        )
        self.store(row)

    def store(self, row):
        with io.open(self.filename, "a") as f:
            f.write(row)

    def parse_line(self, line):
        line = line.strip()
        if line[0] == "#":
            return None, None, line[1:]
        c , mime, name, sha1, length, raw_data = line.split("\t")
        return (BarrelHead(dateutil.parser.parse(c), mime, name, sha1, int(length)), raw_data, None)

    def filter(self, fun=None):
        if not fun:
            fun = lambda x: True
        try:
            with io.open(self.filename, "r") as f:
                for line in f:
                    meta, raw, comment = self.parse_line(line)
                    if not meta:
                        continue
                    if fun(meta):
                        yield(meta, transforms.loads(raw))
        except IOError:
            pass

    def comments(self):
        with io.open(self.filename, "r") as f:
            for line in f:
                _, _, comment = self.parse_line(line)
                if comment:
                    yield comment

    @property
    def meta(self):
        result = BarrelMeta(heads=[], comments=[])

        try:
            with io.open(self.filename, "r") as f:
                for line in f:
                    head, _, comment = self.parse_line(line)
                    if head:
                        result.heads.append(head)
                    if comment:
                        result.comments.append(comment)
        except IOError as e:
            pass
        return result
