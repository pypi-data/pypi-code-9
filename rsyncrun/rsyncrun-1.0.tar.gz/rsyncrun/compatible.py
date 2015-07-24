# -*-coding:utf-8-*-

__all__ = ["Compatible"]

import os


class Compatible(object):

    @staticmethod
    def compatible_with_old_API(runner):
        """ Comptible with xdeploy and rsyncrun

        Old API name is "xdeploy_mvj3.json"
        New API name is "rsyncrun_mvj3.json"

        NOTE:
          1. old project is http://github.com/17zuoye/xdeploy
        """
        runner.should_compatible_with_old_API = False

        if find_old_api(runner):
            runner.should_compatible_with_old_API = True
            runner.conf_file = runner.old_api_json_filename
        return runner


def find_old_api(runner):
    if not os.path.exists(runner.conf_file):
        if os.path.exists(runner.old_api_json_filename):  # backward
            return True
    return False
