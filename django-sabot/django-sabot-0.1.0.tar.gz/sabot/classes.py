from __future__ import unicode_literals

from django.utils.module_loading import import_string


class Patcher(object):
    """
    Base class that allow monkey patching parts of Django by passing it the
    `path` to the module.class and `method_name` of that class to be patched
    """

    path = None
    method_name = None

    def init(self):
        parent = import_string(self.path)
        old_method = getattr(parent, self.method_name)
        setattr(parent, self.method_name, self.return_patched(old_method))
        self.post_patch()

    def post_patch(self):
        return
