from __future__ import (unicode_literals, division,
                        absolute_import, print_function)


from reggae.build import Target, Dependencies, FixedDependencies, dependencies


def object_files(src_dirs=[],
                 exclude_dirs=[],
                 src_files=[],
                 exclude_files=[],
                 flags='',
                 includes=[],
                 string_imports=[]):

    if any(not isinstance(x, list) for x in
           (src_dirs, exclude_dirs, src_files, exclude_files,
            includes, string_imports)):
        raise TypeError("All arguments except flags must be lists")

    if not isinstance(flags, str):
        raise TypeError("flags must be a string")

    return DynamicDependencies('objectFiles',
                               src_dirs=src_dirs,
                               exclude_dirs=exclude_dirs,
                               src_files=src_files,
                               exclude_files=exclude_files,
                               flags=flags,
                               includes=includes,
                               string_imports=string_imports)


class Dynamic(object):
    def __init__(self, func_name, **kwargs):
        self.func_name = func_name
        self.kwargs = kwargs

    def jsonify(self):
        base = {'type': 'dynamic', 'func': self.func_name}
        for k, v in self.kwargs.items():
            if hasattr(v, 'jsonify'):
                base[k] = v.jsonify()
            else:
                base[k] = v
        return base


class DynamicDependencies(Dynamic, Dependencies):
    def __init__(self, func_name, **kwargs):
        self.func_name = func_name
        self.kwargs = kwargs

    def jsonify(self):
        base = {'type': 'dynamic', 'func': self.func_name}
        base.update(self.kwargs)
        return base


def link(exe_name=None, flags='', dependencies=None, implicits=[]):
    assert exe_name is not None
    assert dependencies is not None
    return Target([exe_name], LinkCommand(flags), dependencies, implicits)


class LinkCommand(object):
    def __init__(self, flags=''):
        self.flags = flags

    def jsonify(self):
        return {'type': 'link', 'flags': self.flags}


def static_library(name,
                   src_dirs=[],
                   exclude_dirs=[],
                   src_files=[],
                   exclude_files=[],
                   flags='',
                   includes=[],
                   string_imports=[]):

    assert name is not None

    return DynamicDependencies('staticLibrary',
                               name=name,
                               src_dirs=src_dirs,
                               exclude_dirs=exclude_dirs,
                               src_files=src_files,
                               exclude_files=exclude_files,
                               flags=flags,
                               includes=includes,
                               string_imports=string_imports)


def scriptlike(src_name=None,
               exe_name=None,
               flags='',
               includes=[],
               string_imports=[],
               link_with=[]):
    assert src_name is not None
    assert exe_name is not None

    return Dynamic('scriptlike',
                   src_name=src_name,
                   exe_name=exe_name,
                   flags=flags,
                   includes=includes,
                   string_imports=string_imports,
                   link_with=dependencies(link_with, FixedDependencies))
