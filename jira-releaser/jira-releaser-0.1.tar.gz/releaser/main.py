# -*- coding: UTF-8 -*-
from releaser import dialog

repo_urls = dialog.get_repository()

if len(repo_urls) == 0:
    print "We need one or more git repository"
    exit()

master_branch = dialog.get_master_branch()
jira_username = dialog.get_jira_user()
jira_password = dialog.get_jira_password()
fix_version = dialog.get_fix_version()

