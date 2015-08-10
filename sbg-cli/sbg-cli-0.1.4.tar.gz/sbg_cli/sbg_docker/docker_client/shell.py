__author__ = 'Sinisa'

import os
import uuid

CID_DIR = '/tmp/'


class Shell(object):

    def run_shell(self):
        raise NotImplementedError(self._message('run_shell'))

    def _message(self, method):
        return "Method '%s' not implemented for class %s." % method, self.__class__.__name__


class Bash(Shell):

    def __init__(self, dir, image):
        self.cid_file = os.path.join(CID_DIR, 'cid_%s' %str(uuid.uuid4()))
        self.dir = dir
        self.image_id = image

    def run_shell(self):
        pid = os.fork()
        if not pid:
            self.sh()
        else:
            os.wait()
            with open(self.cid_file) as cid_file:
                cid = cid_file.read()
            os.remove(self.cid_file)
            return cid

    def sh(self):
        args = ['docker', 'run', '-i', '-t']
        args += ['-v', '%s:/mountedcwd:rw' % self.dir]
        args += ['--cidfile', self.cid_file]
        args += [self.image_id]
        args += ['/bin/bash']

        os.execvp('docker', args)

