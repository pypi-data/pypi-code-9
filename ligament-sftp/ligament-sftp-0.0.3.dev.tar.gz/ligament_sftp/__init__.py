""" Simple SFTP support for the `ligament` task operator"""
import os
import glob
import json
import pysftp
from ligament.buildtarget import BuildTarget

from ligament.helpers import mkdir_recursive, pdebug, pwarning

COPY = "_COPY"

UPLOAD = "_UPLOAD"
DOWNLAOD ="_DOWNLOAD"

class SftpOperation(BuildTarget):
    """
    Simple SFTP operations as a ligament task
    """

    def __init__(self,
        login_credentials,
        targets,
        destination,
        operation,
        direction=UPLOAD,
        **kwargs):
        """ 
        """
        BuildTarget.__init__(self, **kwargs)

        self.login_credentials = login_credentials

        self.direction = direction
        self.destination = destination
        self.targets = reduce(
            lambda a, b: a + b,
            [glob.glob(x) for x in targets])

    def build(self):
        with pysftp.Connection(**self.login_credentials) as sftp:

            if self.direction == UPLOAD:
                for target in self.targets:
                    sftp_copy_recursive(
                        sftp, 
                        target, 
                        self.destination)
                    
            else:
                raise Exception("sftp download not implemented")


def sftp_copy_recursive(remote, localpath, remotepath,
                        merge=True, replace=True):
    local_isdir = os.path.isdir(localpath)
    remote_exists = remote.exists(remotepath)
    remote_isdir = remote_exists and remote.isdir(remotepath)

    pdebug("sftp %s -> %s" %(localpath, remotepath))

    if remote_exists:
        if remote_isdir:
            if local_isdir and merge:
                # copy each elem in directory over
                for elem in os.listdir(localpath):
                    sftp_copy_recursive(remote, 
                        os.path.join(localpath, elem), 
                        os.path.join(remotepath, elem),
                        merge=merge,
                        replace=replace)

            elif local_isdir and not merge:
                pwarning("not merging files!")

            if not local_isdir:
                # put file in folder
                sftp_copy_recursive(remote, 
                    localpath, 
                    os.path.join(remotepath, 
                        os.path.basename(localpath)),
                    merge=merge,
                    replace=replace)
        else:
            if replace:
                # remove old file and replace it
                remote.remove(remotepath)
                remote.put(localpath, remotepath)
            else:
                pwarning("not replacing file")

    else:
        # just copy it over with the correct pysftp function
        if local_isdir:
            remote.mkdir(remotepath)
            remote.put_r(localpath, remotepath)
        else:
            remote.put(localpath, remotepath)
