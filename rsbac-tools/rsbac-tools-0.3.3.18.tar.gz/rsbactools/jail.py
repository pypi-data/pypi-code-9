# Copyright (C) 2011-2014 Jens Kasten. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 

"""
Jail package for RSBAC JAIL module.

Copyright (C) Jens Kasten. All Rights Reserved.
"""

__author__  = "Jens Kasten <jens@kasten-edv.de>"
__status__  = "beta"
__version__ = "0.4"
__date__    = "08 July 2014"

__all__ = ["RunJail", ]


import os
import sys

import logging
logging.basicConfig(format='%(levelname)s:%(name)s:line %(lineno)s: %(message)s')
log = logging.getLogger(__name__)

try:
    from rsbactools import config, converter, get_pid_from_name, rsbac, which
except ImportError as error:
    raise RuntimeError (error)


# Path where jail config files located
RSBAC_JAIL_CONFIG_DIR = "/etc/rsbac/jail" 

# list of all available jail attribute
RSBAC_JAIL_ATTRIBUTE = [
    'jail_id',
    'jail_ip',
    'jail_flags',
    'jail_max_caps',
    'jail_scd_get',
    'jail_scd_modify'
]


# coresponde with the jail config keys
# { "jail-flags": ["allow-dev-read"] }
# call in rsbactools/jail/helper.py the class JailFlags
RSBAC_JAIL_CLASS_MAPPER = {
    "jail-flags": "JailFlags",
    "max-caps": "JailMaxCaps",
    "scd-get": "JailScdGet",
    "scd-read": "JailScdGet",
    "scd-modify": "JailScdModify",
    "scd-set": "JailScdModify",
    "jail-ip": "JailIp",
    "chroot": "JailChroot",
}



# jail flags value are taken from 
# rsbac/types.h line around 462
RSBAC_JAIL_FLAGS = {
    "allow-external-ipc": (1, "-i"),
    "allow-all-net-family": (2, "-n"),
    "allow-inet-raw": (8, "-r"),
    "auto-adjust-ip-address": (16, "-a"),
    "allow-inet-localhost": (32, "-o"),
    "allow-dev-get-status": (128, "-e"),
    "allow-dev-mod-system": (256, "-E"),
    "allow-dev-read": (512, "-d"),
    "allow-dev-write": (1024, "-D"),
    "allow-tty-open": (2048, "-t"),
    "allow-ipc-parent": (4096, "-P"),
    "allow-suid": (8192, "-s"),
    "allow-mount": (16384, "-u"),
    "this-is-syslog": (32768, "-Y"),
    "allow-ipc-syslog": (65536, "-y"),
    "allow-netlink": (131072, "-K"),
    "allow-netlink-mod-system": (262142, "-k"),
    "virtual-user": ("virtual-user", "-V"),
    "private-namespace": ("private-namsespace", "-N"),
}
       
RSBAC_JAIL_MAX_CAPS = {
    "chown": (0, "CHOWN"),
    "dac-override": (1, "DAC_OVERRIDE"),
    "dac-read-search": (2, "DAC_READ_SEARCH"),
    "fowner": (3, "FOWNER"),
    "fsetid": (4, "FSETID"),
    "kill": (5, "KILL"),
    "setgid": (6, "SETGID"),
    "setuid": (7, "SETUID"),
    "setpcap": (8, "SETPCAP"),
    "linux-immutable": (9, "LINUX_IMMUTABLE"),
    "net-bind-service": (10, "NET_BIND_SERVICE"),
    "net-broadcast": (11, "NET_BROADCAST"),
    "net-admin": (12, "NET_ADMIN"),
    "net-raw": (13, "NET_RAW"),
    "ipc-lock": (14, "IPC_LOCK"),
    "ipc-owner": (15, "IPC_OWNER"),
    "sys-module": (16, "SYS_MODULE"),
    "sys-rawio": (17, "SYS_RAWIO"),
    "sys-chroot": (18, "SYS_CHROOT"),
    "sys-ptrace": (19, "SYS_PTRACE"),
    "sys-pacct": (20, "SYS_PACCT"),
    "sys-admin": (21, "SYS_ADMIN"),
    "sys-boot": (22, "SYS_BOOT"),
    "sys-nice": (23, "SYS_NICE"),
    "sys-resource": (24, "SYS_RESOURCE"),
    "sys-time": (25, "SYS_TIME"),
    "sys-tty-config": (26, "SYS_TTY_CONFIG"),
    "mknod": (27, "MKNOD"),
    "lease": (28, "LEASE"),
    "audit-control": (30, "AUDIT_CONTROL"),
    "audit-write": (29, "AUDIT_WRITE"),
    "setfcap": (31, "SETFCAP"),
}

# cap flags are taken from 
# linux/capabilities.h
# FIXME: get source for int values
RSBAC_JAIL_SCD = {
    "time-strucs": (0, "time_strucs"),
    "clock": (1, "clock"),
    "host-id": (2, "host_id"),
    "net-id": (3, "net_id"),
    "ioports": (4, "ioports"),
    "rlimit": (5, "rlimit"),
    "swap": (6, "swap"),
    "syslog": (7, "syslog"),
    "rsbac": (8, "rsbac"),
    "rsbac-log": (9, "rsbac_log"),
    "other": (10, "other"),
    "kmem": (11, "kmem"),
    "network": (12, "network"),
    "firewall": (13, "firewall"),
    "priority": (14, "priority"),
    "sysfs": (15, "sysfs"),
    "rsbac-remote-log": (16, "rsbac_remote_log"),
    "quota": (17, "quota"),
    "sysctl": (18, "sysctl"),
    "nfsd": (19, "nfsd"),
    "ksyms": (20, "ksyms"),
    "mlock": (21, "mlock"),
    "capability": (22, "capability"),
    "kexec": (23, "kexec"),
    "videomem": (24, "videomem"),
}


class JailFlags(object):
    
    def __init__(self):
        self.params = []

    def get(self, params, config_file):
        for i in params:
            try:
                self.params.append(RSBAC_JAIL_FLAGS[i][1])
            except KeyError as error:
                log.error(error)
                sys.stderr.write("Not valid value in '%s' for 'jail-flags'\n" % config_file)
                sys.stderr.write("Available jail-flags:\n")
                for i in sorted(RSBAC_JAIL_FLAGS):
                    sys.stderr.write("%-21s %-21s\n" % ("", i))
                sys.exit(21)
        return self.params


class JailChroot(object):
    
    def __init__(self):
        self.params = ["-R"]

    def get(self, params, config_file):
        self.params.append(params)
        return self.params


class JailIp(object):
    
    def __init__(self):
        self.params = ["-I"]

    def get(self, params, config_file):
        self.params.append(params)
        return self.params


class JailMaxCaps(object):
    
    def __init__(self):
        self.params = ["-C"]

    def get(self, params, config_file):
        for i in params:
            try:
                self.params.append(RSBAC_JAIL_MAX_CAPS[i][1])
            except KeyError as error:
                log.error(error)
                sys.stderr.write("Not valid value in '%s' for 'max-caps'" % config_file)
                sys.stderr.write("Available max-caps:")
                for i in sorted(RSBAC_JAIL_MAX_CAPS):
                    sys.stderr.write("%-21s %-21s" % ("", i))
                sys.exit(22)
        return self.params


class JailScdGet(object):
    
    def __init__(self):
        self.params = ["-G"]

    def get(self, params, config_file):
        for i in params:
            try:
                self.params.append(RSBAC_JAIL_SCD[i][1])
            except KeyError as error:
                log.error(error)
                sys.stderr.write("Not valid value in '%s' for 'scd-get'" % config_file)
                sys.stderr.write("Available scd-get:")
                for i in sorted(RSBAC_JAIL_SCD):
                    sys.stderr.write("%-21s %-21s" % ("", i))
                sys.exit(23)
        return self.params


class JailScdModify(object):
    
    def __init__(self):
        self.params = ["-M"]

    def get(self, params, config_file):
        for i in params:
            try:
                self.params.append(RSBAC_JAIL_SCD[i][1])
            except KeyError as error:
                log.error(error)
                sys.stderr.write("Not valid value in '%s' for 'scd-modify'" % config_file)
                sys.stderr.write("Available scd-modify:")
                for i in sorted(RSBAC_JAIL_SCD):
                    sys.stderr.write("%-21s %-21s" % ("", i))
                sys.exit(24)
        return self.params


class JailParams(object):

    def __init__(self):
        self.params = []

    def set_log_level(self, log_level):
        log.setLevel(log_level)

    def build(self, policies, config_file):
        for key in policies.keys():
            try:
                log.debug("call: %s()" % RSBAC_JAIL_CLASS_MAPPER[key])
                obj = getattr(sys.modules[__name__], RSBAC_JAIL_CLASS_MAPPER[key])()
                log.debug("set: %s" % policies[key])
                params = obj.get(policies[key], config_file)
                log.debug("get: %s" % params)
                self.params += params
            except KeyError as error:
                log.error(error)
                sys.stderr.writer("Could not found ClassName: %s" % key)
                sys.exit(20)
        return True
       
    def get(self):
        return self.params


class RunJail(object):
    """Tool to configure a rsbac_jail through a json configuration file."""

    def __init__(self, args):
        self.args = args
        self.policies = {}
        self.params = []
        if "dry_run" in args and args["dry_run"]:
            self.set_log_level(logging.INFO)
        if "verbose" in args and args["verbose"]:
            self.set_log_level(logging.DEBUG)

    def set_log_level(self, log_level):
        log.setLevel(log_level)

    def get_log_level(self):
        return log.getEffectiveLevel()

    def set_policies(self, config_file):
        log.debug("loading config: %s" % config_file)
        jl = config.JsonLoader()
        jl.set_log_level(self.get_log_level())
        if jl.add_config(config_file) and jl.load_config():
            self.policies = jl.get_values()
            log.debug("loading values: %s" % self.policies)
            return True
        else:
            return False

    def get_policies(self):
        return self.policies
    
    def set_params(self, config_file):
        p = JailParams()
        p.set_log_level(self.get_log_level())
        if not p.build(self.get_policies(), config_file):
            return False
        else:
            self.params = p.get()
            log.debug("converted values: %s" % self.params)
            return True

    def get_params(self):
        return self.params 

    def run(self):
        args = []
        if not "program" in self.args:
            log.error("missing key 'program' in args")
            return False
        if rsbac.Rsbac().get_module("JAIL") == "on":
            log.debug("running in jail mode")
            prog = which("rsbac_jail")
            if not prog:
                sys.stderr.write("Could not found: %s" % rsbac_jail)
                sys.exit(10)
            args.append(prog)
            if "config_file" in self.args and self.args["config_file"]:
                config_file = os.path.join(RSBAC_JAIL_CONFIG_DIR, 
                    ".".join([self.args["config_file"], "json"]))
                if not self.set_policies(config_file):
                    return False
                if not self.set_params(config_file):
                    return False
                args += self.get_params()
        else:
            log.debug("running not in jail mode")
            prog = which(self.args["program"][0])
            if not prog:
                sys.stderr.write("Could not found: %s" % self.args["program"][0])
                sys.exit(11)
        log.debug("Program to execute: %s" % prog)
        prog_to_jail = which(self.args["program"][0])
        if not prog_to_jail:
            sys.stderr.write("Could not found: %s" % self.args["program"][0])
            sys.exit(11)
        args.append(prog_to_jail)
        args += self.args["program"][1:]
        log.debug("Command to execute: %s" % args)
       
        if "dry_run" in self.args and self.args["dry_run"]:
            log.info(" ".join([i for i in args]))
            return True
        try:
            os.execv(prog, args)
            return True
        except OSError as error:
            log.error(error)
            sys.stderr.write(error)
            sys.exit(1)


class PsJail(object):
    """Class to display process jail information."""

    def __init__(self):
        self.processes = {}
        self.processes_info = {}
        self.converter = converter.Converter()

    def list_process(self, prog_name):
        """Search for pid and add them to dictionary."""
        pid = get_pid_from_name(prog_name)
        if pid:
            self.processes[str(pid)] = prog_name
            return True
        else:
            return False

    def list_processes(self):
        """Search for pid in proc directory."""
        for pid in os.listdir("/proc"):
            if pid.isdigit():
                status = os.path.join("/proc", pid, "status")
                with open(status, "r") as fd:   
                    try:
                        name = fd.readline()
                        # add pid as key and processname as value for dict processes
                        self.processes[pid] = name[6:].strip() 
                    except PermissionError as error:
                        pass
                    except OSError as error:
                        pass

    def get_processes_info(self, jail_id_only=False):
        """Collect all available information from rsbac jail."""
        rsbac_api = rsbac.Rsbac()

        # collect all jail infos 
        for pid, process_name in self.processes.items():
            # first get jail_id to test if further action is needed
            jail_id, error = rsbac_api.attr_get_process("JAIL", pid, "jail_id")
            if error:
                continue
            # check if jail_id greater then zero, that process is in jail
            jail_id = jail_id.strip()
            if int(jail_id) == 0:
                continue
            if jail_id_only and jail_id_only != int(jail_id):
                continue
            # assign values to dict    
            self.processes_info[process_name] = {
                "jail_id": jail_id,
                "pid": pid,
            }
          
            for attribute in RSBAC_JAIL_ATTRIBUTE:
                # dont query for jail_id again because already get
                if attribute == "jail_id":
                    continue
                attr, errors = rsbac_api.attr_get_process("JAIL", pid, attribute)
                if error:
                    continue
                if attribute == "jail_ip":
                    self.processes_info[process_name][attribute] = attr.strip()
                elif int(attr) > 0:
                    # get human readable names
                    names = self.get_names_from_number(attribute, attr)
                    self.processes_info[process_name][attribute] = names

    def get_names_from_number(self, attribute, number):
        """Return a list of human readable names."""
        names = []
        if attribute == "jail_flags":
            numbers = self.converter.int_to_bin(number, 32)
            for name, key in RSBAC_JAIL_FLAGS.items():
                if key[0] in numbers:
                    names.append(name)
            return names
        elif attribute == "jail_max_caps":
            numbers = self.converter.bin_to_int(number)
            for name, key in RSBAC_JAIL_MAX_CAPS.items():
                if key[0] in numbers:
                    names.append(name)
            return names
        else:
            numbers = self.converter.bin_to_int(number)
            for name, key in RSBAC_JAIL_SCD.items():
                if key[0] in numbers:
                    names.append(name)
            return names
    
    def show(self):
        """Show the collection information on a terminal with 80 char wide."""
        header = {}
        header["jail_flags"] = "Jail-Flags"
        header["jail_max_caps"] = "Jail-Max-Caps"
        header["jail_scd_get"] = "Jail-SCD-Get"
        header["jail_scd_modify"] = "Jail-SCD-Modify"

        if len(self.processes_info.items()) == 0:
            return 
        
        for process_name, value in sorted(self.processes_info.items()):
            print("-" * 79)
            print("%-18s  Pid: %-6s  Jail Id: %-6s  Jail Ip: %-16s" % (
                process_name, value["pid"], value["jail_id"], value["jail_ip"]))
            print("-" * 79)

            if "jail_flags" in value:
                jail_flags = sorted(value["jail_flags"])
                first = jail_flags[0]
                del jail_flags[0]
                print("%-15s: %s" % (header["jail_flags"], first))
                for i in jail_flags:
                    print("%-16s %s" % ("", i))

            if "jail_max_caps" in value:
                jail_max_caps = sorted(value["jail_max_caps"])
                first = jail_max_caps[0]
                del jail_max_caps[0]
                print("%-15s: %s" % (header["jail_max_caps"], first))
                for i in jail_max_caps:
                    print("%-16s %s" % ("", i))
            if "jail_scd_get" in value:
                jail_scd_get = sorted(value["jail_scd_get"])
                first = jail_scd_get[0]
                del jail_scd_get[0]
                print("%-15s: %s" % (header["jail_scd_get"], first))
                for i in jail_scd_get:
                    print("%-16s %s" % ("", i))
            if "jail_scd_modify" in value:
                jail_scd_modify = sorted(value["jail_scd_modify"])
                first = jail_scd_modify[0]
                del jail_scd_modify[0]
                print("%-15s: %s" % (header["jail_scd_modify"], first))
                for i in jail_scd_modify:
                    print("%-16s %s" % ("", i))

