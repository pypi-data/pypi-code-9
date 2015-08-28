
import os, subprocess, time
from bl.dict import Dict

class File(Dict):
    def __init__(self, fn=None, **args):
        Dict.__init__(self, fn=fn, **args)

    def __repr__(self):
        return "%s(fn=%r)" % (
            self.__class__.__name__, self.fn)

    def open(self):
        subprocess.call(['open', fn], shell=True)

    def read(self, mode='rb'):
        with open(self.fn, mode) as f: 
            data=f.read()
        return data

    def tempfile(self, mode='wb', **args):
        "write the contents of the file to a tempfile and return the tempfile filename"
        with tempfile.NamedTemporaryFile(mode=mode) as tf:
            tfn = tf.name
        self.write(tf.name, mode=mode, **args)
        return tfn

    def write(self, fn=None, data=None, mode='wb', 
                max_tries=3):                   # sometimes there's a disk error on SSD, so try 3x
        outfn = fn or self.fn
        if not os.path.exists(os.path.dirname(outfn)):
            os.makedirs(os.path.dirname(outfn))
        def try_write(b=None, tries=0):         
            try:
                if b is None:
                    b=self.read(mode=mode)
                with open(outfn, mode) as f:
                    f.write(b)
            except: 
                if tries < max_tries:
                    time.sleep(.1)              # I found 0.1 s gives the disk time to recover. YMMV
                    try_write(tries=tries+1)
                else:
                    raise
        try_write(b=data, tries=0)
