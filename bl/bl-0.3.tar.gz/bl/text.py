
import os, shutil, tempfile
from bl.file import File

class Text(File):

    def __init__(self, fn=None, text=None, encoding='UTF-8', **args):
        File.__init__(self, fn=fn, encoding=encoding, **args)
        if text is not None:
            self.text = text
        elif fn is not None and os.path.exists(fn):
            self.text = self.read().decode(encoding)
        else:
            self.text = ""

    def write(self, fn=None, text=None, encoding=None, **args):
        data = (text or self.text or '').encode(encoding or self.encoding)
        File.write(self, fn=fn, data=data, **args)
        
