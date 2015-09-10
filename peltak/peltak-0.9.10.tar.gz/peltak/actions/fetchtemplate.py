# -*- coding: utf-8 -*-
from peltak.actions import actions
from peltak.common.utils import fetch_template
from peltak.config import MR_TEMPLATE_PATH
from peltak.core import cstr


@actions.register(
    'fetch-template',
    desc=("Fetch template from gitlab issue. The issue title and label can "
          "be defined in the config using 'issue_title' and 'issue_label'.")
)
def action_fetchtemplate(app):
    app.authenticate()

    template = fetch_template(app)
    if template is None:
        print(cstr('\n'.join([
            "^31No issue with title ^1{title}^0 ^31and label ^1{label}^0",
            "",
            "You can customize the title and label to search for with",
            "the following ",
            "^1mr_template_title^0",
            "^1issue_label^0."
        ]).format(
            title = app.conf.mr_template_title,
            label = app.conf.issue_label
        )))
    else:
        with open(MR_TEMPLATE_PATH, 'w') as fp:
            fp.write(template)
        print(template)


