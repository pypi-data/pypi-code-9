#
# function that return the backup commands
# only with prefix backup_ in name        
#

import os
import sys
import re
import argparse
import time
import datetime
from subprocess import Popen, PIPE

import logging
logging.basicConfig(format='%(levelname)s:%(name)s:line %(lineno)s: %(message)s')
log = logging.getLogger(__name__)

try:
    from rsbactools import rsbac, RSBAC_PROC_INFO_DIR
except ImportError as error:
    sys.exit(error)


# timestamp
TIMESTAMP = str("%0.f" % datetime.datetime.now().timestamp())
# default backup directory
BACKUP_DIRECTORY = os.path.join(os.getcwd(), "backup")
BACKUP_DIRECTORY_TODAY = os.path.join(
        str(datetime.datetime.now().year),
        str(datetime.datetime.now().month),
        str(datetime.datetime.now().day)
)

# BACKUP_MODULES contains module names which have no entry in 
# /proc/rsbac-info/active or similar
BACKUP_MODULES = ["general", "net", "log"]

# BACKUP_MODULES_EXCLUDE contains module names which are not backup.
#   e.g. JAIL is only process based
BACKUP_MODULES_EXCLUDE = ["JAIL"]
# directories which exclude
DIRECTORIES_EXCLUDE = ["/rsbac.dat", "/proc", "/sys"]

# buffer size for Popen and or open
BUFFER_SIZE = 4096


# command function must return a list 
def command_log():
    cmd = [
        ["switch_adf_log", "-b"]
    ]
    return cmd

def command_net():
    return [
        ["net_temp", "-a", "-b"],
        ["attr_back_net", "-a", "NETDEV"],
        ["attr_back_net", "-a", "NETTEMP"]
    ]

def command_mac():
    return [
        ["mac_back_trusted", "-r", "/"],
        ["attr_back_user", "-a", "-M", "MAC"]
    ]

def command_auth():
    return [
        ["auth_back_cap", "-r", "/"],
        ["attr_back_user", "-a", "-M", "AUTH"]
    ]

def command_cap():
    cmd = [
        ["attr_back_user", "-a", "-M", "CAP"]
    ]
    return cmd

def command_rc():
    return [
        ["rc_get_item", "backup"],
        ["attr", "-a", "-M", "RC"]
    ]

def command_acl():
    acl_tlist_all = call(["acl_tlist", "-n"])
    all_temp = call(["net_temp", "list_temp_nr"])
    cmd = [
        ["acl_tlist", "-br", "FD", ":DEFAULT:", "/"],
        ["acl_tlist", "-b", "DEV", ":DEFAULT:"],
        ["acl_tlist", "-Db"],
        ["acl_tlist", "-br", "IPC", ":DEFAULT:"],
        ["acl_tlist", "-br", "SCD", ":DEFAULT:", acl_tlist_all],
        ["acl_tlist", "-ab"],
        ["acl_tlist", "-br", "PROCESS", ":DEFAULT:"],
        ["acl_tlist", "-br", "NETDEV", ":DEFAULT:"],
        ["acl_tlist", "-br", "NETTEMP_NT", ":DEFAULT:", all_temp],
        ["acl_tlist", "-br", "NETTEMP", all_temp],
        ["acl_tlist", "-br", "NETOBJ", ":DEFAULT:"],
        ["acl_mask", "-br", "FD", "/"],
        ["acl_mask", "-Db"],
        ["acl_mask", "-ab"],
        ["acl_mask", "-b", "SCD", acl_tlist_all]
        ["acl_group", "-gb", "list_groups"]
    ]
    process1 = Popen(["acl_group", "-gs", "list_groups"], stdout=PIPE, 
            stderr=PIPE)
    process2 = Popen(["cut", "-f", "1", "-d", " "], stdin=process1.stdout, 
            stdout=PIPE, stderr=PIPE)
    groups, error = process2.communictate()
    if groups != "":
        for group in groups:
            cmd.append(["acl_group", "-b", "get_group_members", group])
    return cmd

def command_general():
    cmd = []
    for module, status in rsbac.Rsbac().get_modules()["Module"].items():
        if module in BACKUP_MODULES_EXCLUDE:
            continue
        if status == "on":
            cmd.append(["attr_back_dev", "-b"])
    return cmd

def command_um():
    return [
        ["rsbac_groupshow", "-S", "all", "-b", "-p", "-a"],
        ["rsbac_usershow", "-S", "all", "-b", "-p", "-a"]
    ]
    
def command_res():
    #cmd = [attr_get_user RES 4294967292 res_min]
    cmd = [
        ["attr_back_fd", "-r", "-M", "RES", "/"],
        ["attr_back_user", "-a", "-M", "RES"]
    ]
    return cmd

def command_pax():
    cmd = [
        ["attr_back_fd", "-r", "-M", "PAX", "/"],
        ["attr_back_user", "-a", "-M", "PAX"]
    ]
    return cmd

def command_gen():
    cmd = [
        ["attr_back_fd", "-r", "-M", "GEN", "/"],
        ["attr_back_user", "-a", "-M", ""]
    ]
    return cmd

def get_directories(directory="/"):
    directories = os.listdir(directory)
    #for i i

def command(module, directory=["/"]):
    cmd = [
        ["attr_back_fd", "-r", "-M", module, directory],
        ["attr_back_user", "-a", "-M", module]
    ]
    return cmd


class Backup(object):
    """Backup RSABAC attribute modules based."""

    def __init__(self):
        self.args = {}
        self.backup_directory = BACKUP_DIRECTORY
        self.backup_modules = BACKUP_MODULES

    def set_args(self, args):
        self.args = args

    def set_log_level(self, log_level):
        log.setLevel(log_level)

    def get_log_level(self):
        return log.getEffectiveLevel()

    def modules_to_backup(self):
        """Get available modules and extend the module list."""
        modules = self.backup_modules
        try:
            for module, status in rsbac.Rsbac().get_modules()["Module"].items():
                if status == "on":
                    modules.append(module.lower())
            if os.path.exists(os.path.join(RSBAC_PROC_INFO_DIR, "stats_um")):
                modules.append("um")
        except Exception as error:
             log.error(error)
        return modules

    def execute(self, backup_directory_module, module):
        """Execute the module command and write to different files the result.
            The name are build: 
                backup_timestamp.sh
                command_timestamp.sh
                error_timestamp.txt
        """
        # build function name and call the function to get the shell commands
        cmd = globals()["_".join(["command", module])]()

        # build names for writing outupt 
        backup = os.path.join(backup_directory_module, 
                "backup_" + TIMESTAMP + ".sh")
        error = os.path.join(backup_directory_module, 
                "error_" + TIMESTAMP + ".txt")
        command = os.path.join(backup_directory_module, 
                "command_" + TIMESTAMP + ".sh")
       
        try:
            with open(backup, "w", buffering=BUFFER_SIZE) as backup_fd, \
                    open(error, "w", buffering=BUFFER_SIZE) as error_fd, \
                    open(command, "w", buffering=BUFFER_SIZE) as command_fd:
                for i in cmd:
                    command_fd.write(" ".join([str(x) for x in i]) + "\n")
                    process = Popen(i, bufsize=BUFFER_SIZE, stdin=PIPE, 
                            stdout=backup_fd, stderr=error_fd)
                    process.wait()
        except IOError as error:
            log.error(error)
   

    def run(self):
        backup_directory = self.args.get("backup_directory", 
                self.backup_directory)
        backup_directory = os.path.join(backup_directory, 
                BACKUP_DIRECTORY_TODAY)

        for module in self.modules_to_backup():
            # check if full not set 
            if self.args.get("full", False) is False:
                # check if module is set as argument and is True
                if module not in self.args:
                    continue
                elif not self.args[module]:
                    continue
            try:
                backup_directory_module = os.path.join(backup_directory, 
                    module)
                try:
                    log.info("create backup path: %s" % backup_directory_module)
                    os.makedirs(backup_directory_module)
                except OSError as error:
                    log.error(error)
                log.info("starting backup: %s" % module)
                self.execute(backup_directory_module, module)
                log.info("done ...")
            except KeyError as error:
                log.error(error)
                log.error("Not implemented: %s()" % module)
        return True

         
