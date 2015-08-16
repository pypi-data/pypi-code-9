#
# API for python binding of rsbac
# In then moment just placeholder
#

import os
import sys
from subprocess import Popen, PIPE

try:
    from rsbactools import RSBAC_PROC_INFO_DIR
except ImportError as error:
    print(error)
    sys.exit(-1)


class Rsbac(object):
    """Should later replaced by C implementation."""
    
    def __init__(self, verbose=False):
        self.module_on = []
        self.module_off = []
        self.verbose = verbose

    def is_rsbac(self):
        """Simply check if proc directory has subdirectory rsbac."""
        if os.path.isdir(RSBAC_PROC_INFO_DIR):
            return True

    def execute(self, cmd, *args):
        """Generic methode to call Popen().
        Return the result.
        """
        if isinstance(cmd, str):
            cmd = [cmd]
        for i in args:
            if isinstance(i, list):
                cmd.extend(i)
            elif isinstance(i, str):
                cmd.append(i)
        if self.verbose:
            print(" ".join(cmd))
        try:
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            output, error = process.communicate()
            if process.returncode != 0:
                output = output.decode("utf-8").strip()
                return (output, True)
            elif len(error) > 0:
                if error:
                    error = error.decode("utf-8").strip()
                return (error, True)
            else:
                if output:
                    output = output.decode("utf-8").strip()
                return (output, False)
        except IOError as error:
            return (False, "Failure: %s" % error)
  
    def attr_set_fd(self, *args):
        return self.execute("attr_set_fd", *args)
   
    def attr_get_fd(self, *args):
        return self.execute("attr_get_fd", *args)

    def attr_set_user(self, *args):
        return self.execute("attr_set_user", *args)
   
    def attr_get_user(self, *args):
        return self.execute("attr_get_user", *args)

    def attr_set_file_dir(self, *args):
        return self.execute("attr_set_file_dir", *args)
    
    def attr_get_file_dir(self, *args):
        return self.execute("attr_get_file_dir", cmd, *args)

    def rc_set_item(self, *args):
        return self.execute("rc_set_item", *args)

    def rc_get_item(self, *args):
        return self.execute("rc_get_item", *args)

    def rc_copy_type(self, *args):
        return self.execute("rc_copy_type", *args)

    def attr_get_process(self, *args):
        return self.execute("attr_get_process", *args)

    def attr_back_fd(self, *args):
        return self.execute("attr_back_fd", *args)

    def auth_back_cap(self, *args):
        return self.execute("auth_back_cap", *args)
    
    def acl_tlist(self, *args):
        return self.execute("acl_tlist", *args)

    def acl_mask(self, *args):
        return self.execute("acl_mask", *args)

    def get_modules(self, active=False):
        """Retun rsbac module as a dictonary.
        set self.module_on as list with all active module
        set self.module_off as list with all deactive module
        return rsbac_module 
        """
        result = {"Module": {}}
        try:
            with open(os.path.join(RSBAC_PROC_INFO_DIR, "active")) as fd:
                for line in fd.readlines():
                    i = line.split(':')
                    # check if a module is available
                    if i[0] == "Module":
                        # clean string and create a list
                        j = i[1].strip("\n").lstrip(" ").split(" ")
                        # remove empty elements from list
                        j = list(filter(None, j))
                        if active is False:
                            result['Module'][j[0]] = j[1].lower()
                        elif active == "on":
                            if j[1].lower() == "on":
                                result['Module'][j[0]] = j[1].lower()
                        elif active == "off":
                            if j[1].lower() == "off":
                                result['Module'][j[0]] = j[1].lower()
            return result
        except IOError as error:
            return result

    def get_module(self, module):
        """Return status on|off or False."""
        try:
            if self.get_modules():
                return self.get_modules()["Module"][module]
        except KeyError as error:
           return False


if __name__ == "__main__":
    r = Rsbac()
    print(r.get_modules())
