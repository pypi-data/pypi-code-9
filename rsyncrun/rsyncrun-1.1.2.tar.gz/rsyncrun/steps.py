# -*-coding:utf-8-*-

__all__ = ["Steps"]

import os
from .json_conf_template import JsonConfTemplate


class Steps(object):
    """
    Steps are extracted from RsyncRun, but they are both share the same context `self`.
    """

    ordered_steps_list = [
        "setup_conf",
        "validate",
        "sync_source_code",
        "prepare_virtualenv",
        "install_package_lazily",
        "run_some_before_scripts",
        "launch_program",
        "clean",
    ]

    def setup_conf(self):
        if not os.path.exists(self.conf_file):
            print """[warn] can't find self.conf_file = "%s" ! Please create one, e.g. %s""" % (
                self.conf_file, JsonConfTemplate.example)
            exit(1)

    def validate(self):
        assert isinstance(self.conf, dict)
        invalid_example_info = "See valid example in conf %s" % JsonConfTemplate.example
        assert "sync_projects" in self.conf, invalid_example_info
        assert "remote_server" in self.conf, invalid_example_info
        conf_file_msg = "Auto detected" if self.guess_conf_file is self.conf_file else "Specified"
        print "** %s config file is %s" % (conf_file_msg, self.conf_file)

    def sync_source_code(self):
        for sync_opts_type in ["local_to_remote", "remote_to_remote"]:
            sync_opt2 = self.conf["sync_projects"][sync_opts_type]
            for project1 in sync_opt2:

                if sync_opts_type == "remote_to_remote":
                    from_addr, to_addr = sync_opt2[project1]
                else:
                    from_addr = sync_opt2[project1][0]
                    to_addr = "%s:%s" % (self.remote_user_host, sync_opt2[project1][1])
                source_code_sync_command2 = """%s %s  %s | tee -a %s """ % \
                    (self.rsync_cmd,
                     from_addr,
                     to_addr,
                     self.rsync_output_file)

                if sync_opts_type == "remote_to_remote":
                    self.shell.remote(source_code_sync_command2)
                else:
                    self.shell.local(source_code_sync_command2)

        # get remote changed content
        self.shell.local("""scp %s:%s %s; cat %s >> %s; rm -f %s; """ % (
            self.remote_user_host,
            self.rsync_output_file,
            self.rsync_output_file_remote,
            self.rsync_output_file_remote,
            self.rsync_output_file,
            self.rsync_output_file_remote))
        self.source_code_sync_result = file(self.rsync_output_file).read()

        self.shell.local("echo rsync_output_file; cat %s" % self.rsync_output_file)
        self.shell.local("rm -f %s" % self.rsync_output_file)

    def prepare_virtualenv(self):
        self.shell.remote("""
        if [ ! -f ENV/bin/activate ]; then
            pip install virtualenv
            virtualenv ENV
        fi;
        """)

    def install_package_lazily(self):
        self.installer.do(self.source_code_sync_result)

    def run_some_before_scripts(self):
        scripts = self.conf.get("scripts_before_run", list())
        scripts = map(lambda s1: s1.strip(), scripts)
        # Ignore comment.
        scripts = filter(lambda s1: not s1.startswith("#"), scripts)

        for script1 in scripts:
            self.shell.remote(script1)

    def launch_program(self):
        task_opts = self.conf["launch"].get("params_list", list())
        if not isinstance(task_opts, list):
            task_opts = [task_opts]
        params_index = self.conf["launch"].get("params_index", 0)
        task_opts = task_opts[params_index]
        self.shell.remote(self.conf["launch"]["template"] % tuple(task_opts))

    def clean(self):
        """ when exit, clean """
        clean_file_under_root_tmp = """
            find /tmp/ -maxdepth 1 -type f -mmin +30 | grep %s | xargs rm -f ;"""
        self.shell.remote(clean_file_under_root_tmp % JsonConfTemplate.name_prefix)
