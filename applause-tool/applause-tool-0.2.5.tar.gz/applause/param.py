import click
from click.types import StringParamType


class PathString(click.Path):
    def convert(self, value, param, ctx):
        if value.startswith("@"):
            with open(super(PathString, self).convert(value[1:], param, ctx), "rb") as afile:
                return afile.read()
        else:
            return StringParamType().convert(value, param, ctx)

    def get_metavar(self, param):
        return "@PATH or TEXT"