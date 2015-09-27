# zip.py - class for handling ZIP files

DEBUG = False

from zipfile import ZipFile, ZIP_DEFLATED
import os
from bl.dict import Dict

class ZIP(Dict):

    def __init__(self, fn, config=None, mode='r', compression=ZIP_DEFLATED):
        Dict.__init__(self, fn=fn, config=config, mode=mode)
        self.zip = ZipFile(self.fn, mode=mode, compression=compression)

    def __repr__(self):
        return "%s('%s', config=%s, mode='%s')" % \
            (self.__class__.__name__, self.fn, self.config, self.mode)
    
    def unzip(self, path=None, members=None, pwd=None):
        if path is None: path = os.path.splitext(self.fn)[0]
        if not os.path.exists(path): os.makedirs(path)
        self.zip.extractall(path=path, members=members, pwd=pwd)

    def close(self):
        self.zip.close()

    @classmethod
    def zip_path(CLASS, path, fn=None, mode='w', exclude=[]):
        if DEBUG==True: print("zip_path():", path)
        if fn is None:
            fn = path+'.zip'
        zipf = CLASS(fn, mode=mode).zip
        for walk_tuple in os.walk(path):
            dirfn = walk_tuple[0]
            for fp in walk_tuple[-1]:
                walkfn = os.path.join(dirfn, fp)
                if DEBUG==True: print('  ', os.path.relpath(walkfn, path))
                if os.path.relpath(walkfn, path) not in exclude:
                    zipf.write(walkfn, os.path.relpath(walkfn, path))
        zipf.close()
        return fn
