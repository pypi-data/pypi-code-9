from pydockerfile.dockerfile import Dockerfile
from pydockerfile.dockerfile import Line


class LineParser(object):
    def __init__(self, line_class=Line):
        self.line_class = line_class

    def from_string(self, string):
        trimmed_string = string.strip()
        if trimmed_string.startswith("#"):
            # We have a comment
            return self.line_class(
                "#", trimmed_string.lstrip("#").strip(), string)
        elif not trimmed_string:
            # Blank line
            return self.line_class("", "", string)
        else:
            # First instance of line continuation, so we have a cmd
            cmd, args = trimmed_string.split(" ", 1)
            return self.line_class(cmd, args, string)


class DockerfileParser(object):
    def __init__(self, dockerfile_class=Dockerfile, line_parser=LineParser):
        self.dockerfile_class = dockerfile_class
        self.line_parser = line_parser()

    def from_file(self, path):
        """Read a Dockerfile at `path`"""
        with open(path, 'r') as f:
            return self._from_iterable(f)

    def from_string(self, string):
        """Parse a Dockerfile from a string"""
        return self._from_iterable(string.strip().split("\n"))

    def _from_iterable(self, iterable):
        dockerfile = self.dockerfile_class()
        for line in self._yield_lines(iterable):
            dockerfile.lines.append(self.line_parser.from_string(line))
        return dockerfile

    def _yield_lines(self, iterable):
        current_line = []
        # Inspired by https://github.com/mpapierski/dockerfile-parser
        for raw_line in iterable:
            string = raw_line.strip()
            if string.startswith("#") or not string:
                yield raw_line.rstrip()
                continue
            current_line.append(string)
            if not string.endswith("\\"):
                yield " ".join(current_line)
                current_line = []


def parse_file(file_path):
    return DockerfileParser().from_file(file_path)
