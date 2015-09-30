from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import banner

import fileinput
import sys
import shutil
import os

class version_incr(object):

    filename = None

    TAG = "version ="
    #TAG = "__version__

    def which(self, name):
        if name.startswith("r"): # release
            return 2
        elif name.startswith("mi"): # minor
            return 1
        elif name.startswith("ma"): # major
            return 0
        else:
            return 2

    def __init__(self, filename, kind="release"):
        self.filename = filename
        self.version = None
        self.position = self.which(kind)

    def find(self):
        old_version = "0.0.0"
        f_in = open(self.filename, "r")
        for line in f_in:
            if line.startswith('version ='):
                v = line.split("=")[1].strip()
                v = v.replace('"', '')
                old_version = v
                self.version = v.split('.')
                break
        return old_version


    def incr(self):
        """reads the version number"""
        print "Changing version in file", self.filename
        f_in = open(self.filename, "r")
        f_out = open("tmp", "w")
        for line in f_in:
            if line.startswith('version ='):
                v = line.split("=")[1].strip()
                v = v.replace('"', '')
                old_version = v
                self.version = v.split('.')
                self.version[self.position] = str(int(self.version[self.position]) + 1)
                new_version = ".".join(self.version)
                f_out.write('version = "{:}"\n'.format(new_version))
            else:
                f_out.write(line)
        f_in.close()
        f_out.close()
        shutil.move("tmp", self.filename)

        print "Changed version from {:} to {:}".format(old_version, new_version)

    def git_commit_needed(self):
        content = Shell.git("status")
        return ("Changes to be committed:" in content) or \
               ('Your branch is ahead' in content)


    def tag(self):
        v = self.find()
        banner("v")
        print v

        #v = ".".join(self.version)
        os.system("python shell_plugins.py install")

        if self.git_commit_needed():
            banner("git commit")
            command = "git commit -m 'version {:}' {:}".format(v,self.filename)
            print "CCC", command
            os.system(command)
            os.system("git push")

        else:
            print "git commit not needed"

        Shell.git("tag", "-a", v, "-m", "version {:}".format(v))
        Shell.git("push", "origin", "--tags")

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        kind = "release"
        v = version_incr(filename, kind=kind)
        v.incr()
    elif sys.argv[2] == 'tag':
        filename = sys.argv[1]
        v = version_incr(filename)
        v.tag()
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        kind = sys.argv[2]
        v = version_incr(filename, kind=kind)
        v.incr()
    else:
        print "usage: cm-incr-version filename (release|minor|major)"
        print "           increments the version number"
        print "usage: cm-incr-version filename tag"
        print "           tags the version in github"







if __name__ == "__main__":
    main()
