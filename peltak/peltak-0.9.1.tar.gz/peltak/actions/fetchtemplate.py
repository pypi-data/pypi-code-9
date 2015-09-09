# -*- coding: utf-8 -*-
from peltak.actions import actions
from peltak.common.utils import fetch_template


@actions.register(
    'fetch-template',
    desc=("Fetch template from gitlab issue. The issue title and label can "
          "be defined in the config using 'issue_title' and 'issue_label'.")
)
def action_fetchtemplate(app):
    fetch_template(app)

