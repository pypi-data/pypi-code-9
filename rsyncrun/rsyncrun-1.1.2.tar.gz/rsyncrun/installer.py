# -*-coding:utf-8-*-

__all__ = ["Installer"]

import os


class Installer(object):
    """
    Give a incremental code changelog, and install relative changed Python package.
    """

    def __init__(self, shell, package_dir_list):
        self.shell = shell
        self.package_dir_list = package_dir_list

    def do(self, incremental_code_changelog):
        """
        `incremental_code_changelog` is lines sync filenames.
        """
        print
        print "[incremental_code_changelog]", incremental_code_changelog
        print

        for pkg in self.package_dir_list:
            pkg_short = pkg.split("/")[-1]  # if has dir
            need_install = pkg in incremental_code_changelog

            if need_install:
                print "[install packaqe]", pkg_short, "is changed ..."
                dir1 = os.path.join(self.shell.execute_dir, pkg)
                self.shell.remote("cd %s; python setup.py install" % dir1)
            else:
                print "[install packaqe]", pkg_short, "is not changed."
