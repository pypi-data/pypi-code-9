import yaml


class BaseTag:
    default_tag_name = None

    def register(self, tag_name=None, loader=yaml.Loader):
        yaml.add_constructor(
            tag_name or self.default_tag_name,
            self.parse,
            loader)

    def parse(self, loader, node):
        raise Exception("not implemented")


class TagParseError(Exception):
    pass
