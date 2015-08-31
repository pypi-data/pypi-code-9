from .base import BaseTag, TagParseError
import os.path
import yaml


class IncTag(BaseTag):
    default_tag_name = "!inc"

    def __init__(self, file_ext=None, basepath=None, inc_file_loader=None):
        self.file_ext = file_ext or ".yaml"
        self.basepath = basepath

        # 若为 None，则使用解析当前文件的 loader，否则使用指定的 loader
        # 例如希望 inc file 本身不能再载入其他 inc file，就可以为其指定一个未注册 inc tag 的 loader
        self.inc_file_loader = inc_file_loader

    def parse(self, loader, node):
        # 取不到文件名时，拿什么作为相对路径？可以使用 getpwd()

        if not isinstance(node.value, str):
            raise TagParseError("yaml tag !inc 的值必须是字符串(got {})".format(node.value))

        path = node.value + self.file_ext
        base = self.basepath or (
            os.path.dirname(loader.name)
            if not os.path.isabs(path) and os.path.isfile(loader.name)
            else ""
        )
        path = os.path.abspath(os.path.join(base, path))

        if not os.path.isfile(path):
            raise TagParseError("yaml tag !inc 指定的文件不存在: {}".format(path))

        loader = self.inc_file_loader or type(loader)
        with open(path) as f:
            return yaml.load(f, loader)
