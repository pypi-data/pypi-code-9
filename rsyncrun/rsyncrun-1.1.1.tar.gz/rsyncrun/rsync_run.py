# -*-coding:utf-8-*-

__all__ = ["RsyncRun"]

import os
import getpass
import argparse
import json
import datetime
from cached_property import cached_property

from .json_conf_template import JsonConfTemplate
from .compatible import Compatible
from .shell import Shell
from .installer import Installer
from .steps import Steps

# TODO mock remote server


class RsyncRun(Steps):
    """
    RsyncRun configration module.

    Executable code are placed in Steps.
    """

    def __init__(self, sys_argv=[]):
        self.argv = sys_argv
        self.pid = os.getpid()
        self.directory = self.args.directory
        self.user = self.args.user

        # e.g. rsyncrun_mvj3.json
        self.guess_conf_file = os.path.join(self.directory, JsonConfTemplate.name_prefix + "_" + self.user + ".json")
        # e.g. xdeploy_mvj3.json
        self.guess_conf_file_old = os.path.join(self.directory, JsonConfTemplate.name_prefix_old + "_" + self.user + ".json")
        # e.g. rsyncrun_luiti_webui.json
        self.specified_conf_file = None
        if self.args.conf:
            if self.args.conf.startswith("/"):
                self.specified_conf_file = self.args.conf
            else:
                self.specified_conf_file = os.path.join(self.directory, self.args.conf)

        self.is_auto_guessed = os.path.exists(self.guess_conf_file)

        self.conf_file = None
        if self.is_auto_guessed:
            self.conf_file = self.guess_conf_file
        if (self.conf_file is None) and os.path.exists(self.guess_conf_file_old):
            self.conf_file = self.guess_conf_file_old
        if os.path.exists(self.specified_conf_file):
            self.conf_file = self.specified_conf_file  # force overwrite above

        assert isinstance(self.conf_file, basestring), self.conf_file
        Compatible.compatible_with_old_API(self)

    def run(self):
        # http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
        def green_line(string):
            """ colorize shell output """
            fg_lightgreen = '\033[92m'
            fg_reset = '\033[0m'
            bg_black = '\033[40m'
            print fg_lightgreen + bg_black + string + fg_reset

        for idx, step in enumerate(self.ordered_steps_list):
            green_line("\n[Step#%s]: %s\n" % (idx + 1, step.replace("_", " ")))
            getattr(self, step)()

    @cached_property
    def shell(self):
        return Shell(self.remote_user_host, self.execute_dir)

    @cached_property
    def installer(self):
        return Installer(self.shell, self.conf["sync_projects"]["projects_lazy_install_by_python"])

    @cached_property
    def old_api_json_filename(self):
        return self.guess_conf_file.replace(JsonConfTemplate.name_prefix, JsonConfTemplate.name_prefix_old)

    @cached_property
    def parser(self):
        parser = argparse.ArgumentParser(description="rsyncrun --- Rsync your code to server and run.")
        parser.add_argument(
            '--directory', default=os.getcwd(),
            help=u"Use this directory to find guessed config json file automately.", required=False, )
        parser.add_argument(
            '--user', default=getpass.getuser(),
            help=u"Use username to find guessed config json file automately.", required=False, )
        parser.add_argument(
            '--conf', default=getpass.getuser(),
            help=u"Force to specify a conf file.", required=False, )
        return parser

    @cached_property
    def args(self):
        return self.parser.parse_args(self.argv[1:])

    @cached_property
    def conf(self):
        return json.loads(file(self.conf_file).read())

    @cached_property
    def rsync_cmd(self):
        # TODO check rsync exists
        base = "rsync -av "  # rsync 不要 -z 选项
        exclude_rules = self.conf["sync_projects"].get("exclude_rules", list())
        for rule1 in exclude_rules:
            base += (" --exclude %s " % rule1)
        return base

    @cached_property
    def execute_dir(self):
        return self.conf["remote_server"]["execute_dir"].rstrip("/")

    @cached_property
    def rsync_output_file(self):
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        return "/tmp/%s_%s_%s" % (JsonConfTemplate.name_prefix, today_str, self.pid)

    @cached_property
    def rsync_output_file_remote(self):
        return "%s_2" % self.rsync_output_file

    @cached_property
    def remote_user_host(self):
        return "%s@%s" % (self.conf["remote_server"]["user"], self.conf["remote_server"]["host"],)
