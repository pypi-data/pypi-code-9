class Line(object):
    def __init__(self, cmd, args, raw):
        self.cmd = cmd
        self.args = args
        self.raw = raw

    def __repr__(self):
        return "<Line({cmd}, {args})>".format(cmd=self.cmd, args=self.args)

    def __str__(self):
        return self.raw

    def __json__(self):
        return {self.cmd: self.args}

    def __eq__(self, other):
        return (self.cmd == other.cmd and
                self.args == other.args and
                self.raw == other.raw)


class Dockerfile(object):
    def __init__(self, line_class=Line):
        self.lines = []
        self._line_class = line_class

    def __repr__(self):
        first_line = self.lines[0] if self.lines else None
        return "<Dockerfile({first_line}...)>".format(
            first_line=str(first_line))

    def __str__(self):
        return "\n".join(str(line) for line in self.lines)

    def __json__(self):
        return [line.__json__() for line in self.lines]

    def __len__(self):
        return len(self.lines)

    def __eq__(self, other):
        return (len(self.lines) == len(other.lines) and
                self._line_class == other._line_class and
                all(l1 == l2 for (l1, l2) in zip(self.lines, other.lines)))

    def __getattr__(self, attr_name):
        return [line for line in self.lines
                if line.cmd.lower() == attr_name.lower()]
