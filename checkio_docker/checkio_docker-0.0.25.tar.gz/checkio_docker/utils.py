import os
import shutil as _shutil
from tempfile import mkdtemp


class TemporaryDirectory(object):
    def __init__(self):
        self.working_path = mkdtemp()
        self._closed = False

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.working_path)

    def __enter__(self):
        return self.working_path

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if not self._closed:
            if os.path.exists(self.working_path):
                _shutil.rmtree(self.working_path)
            self._closed = True


def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), os.path.join(dest, f), ignore)
    else:
        _shutil.copyfile(src, dest)
        os.chmod(dest, 0o755)
