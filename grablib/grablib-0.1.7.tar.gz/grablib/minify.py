import os
import re
import shutil

from jsmin import jsmin
from csscompressor import compress as cssmin

from .common import ProcessBase, GrablibError, basestring

MINIFY_LOOKUP = [
    (r'.js$', jsmin),
    (r'.css$', cssmin),
]


class MinifyLibs(ProcessBase):
    """
    minify and concatenate js and css
    """

    def __init__(self, minify_info, **kwargs):
        """
        initialize MinifyLibs.
        :param minify_info: dict of: files to generate => list of regexes of files to generate it from
        :param sites: dict of names of sites to simplify similar urls, see examples.
        """
        super(MinifyLibs, self).__init__(**kwargs)
        self.minify_info = minify_info

    def __call__(self):
        """
        alias to minify
        """
        return self.minify()

    def minify(self):
        grablib_files = list(self.grablib_files())
        if os.path.exists(self.minified_root):
            self.output('minified root directory "%s" already existing, deleting' % self.minified_root, 1)
            shutil.rmtree(self.minified_root)
        for dst, srcs in self.minify_info.items():
            if not isinstance(srcs, list):
                raise GrablibError('minifying: strange type of src_files: %s' % type(srcs))

            final_content = ''
            files_combined = 0
            for src in srcs:
                content = ''
                if not isinstance(src, basestring):
                    # here we assume we have a 2 element list, first item being the src, second be a dict of regexes
                    src, regexes = src
                else:
                    regexes = None
                if src.startswith('./') and os.path.exists(src):
                    content = self._minify_file(src)
                    files_combined += 1
                else:
                    for file_path, _ in self._search_paths(grablib_files, src):
                        full_file_path = os.path.join(self.download_root, file_path)
                        content = self._minify_file(full_file_path)
                        files_combined += 1
                if regexes:
                    for pattern, rep in regexes.items():
                        content = re.sub(pattern, rep, content)
                final_content += content
            if files_combined == 0:
                self.output('no files found to form "%s"' % dst, 1)
                continue
            _, dst = self._generate_path(self.minified_root, dst)
            self._write(dst, final_content)
            self.output('%d files combined to form "%s"' % (files_combined, dst), 2)
        return True

    def grablib_files(self):
        """
        get a list of file paths in the libs root directory
        """
        root_dir_length = None
        for root, _, files in os.walk(self.download_root):
            if root_dir_length is None:
                root_dir_length = len(root)
            for f in files:
                file_path = os.path.join(root, f)
                # we have to strip off the root directory to ease setting up source
                file_path = file_path[root_dir_length:].lstrip('/')
                yield file_path

    @classmethod
    def _minify_file(cls, file_path):
        if file_path.endswith('.js'):
            return cls._jsmin_file(file_path)
        elif file_path.endswith('.css'):
            return cls._cssmin_file(file_path)

        with open(file_path) as original_file:
            return original_file.read()

    @staticmethod
    def _jsmin_file(file_path):
        with open(file_path) as original_file:
            return jsmin(original_file.read())

    @staticmethod
    def _cssmin_file(file_path):
        with open(file_path) as original_file:
            return cssmin(original_file.read())
