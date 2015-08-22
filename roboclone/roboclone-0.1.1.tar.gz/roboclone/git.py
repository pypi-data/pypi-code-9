import os
import re


class GitCloneError(Exception):
    def __init__(self, message):
        self.message = message


class Repository:
    def __init__(self, url):
        self.url = url
        self.name = re.findall(r".+/(.+)\.git?", self.url)[0]

    def clone(self, outdir, args=None):
        if outdir is None:
            outdir = self.name
        if args is None:
            args = ''
        status = os.system("git clone {url} {outdir} {args}".format(url=self.url, outdir=outdir, args=args))
        if status != 0:
            raise GitCloneError("Running of git-clone failed with status code {}".format(status))