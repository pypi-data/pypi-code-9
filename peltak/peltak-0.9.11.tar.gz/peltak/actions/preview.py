# -*- coding: utf-8 -*-
import os.path
from peltak.actions import actions
from peltak.config import MR_TEMPLATE_PATH, MR_CACHE_PATH
from peltak.common import prompt
from peltak.common.cache import CachedObj
from peltak.common.utils import resetmr_if_closed
from peltak.core.template import Template


@actions.register(
    'preview',
    desc="Prints the preview of the merge request in its current state."
)
def action_preview(app):
    app.authenticate()
    resetmr_if_closed(app)
    mrcache = CachedObj.load_file(MR_CACHE_PATH)
    if os.path.exists(MR_TEMPLATE_PATH):
        template = Template.load_from_file(MR_TEMPLATE_PATH)
        template.fill(mrcache)
        mrcache.description = template.render()
    prompt.print_mr(app, mrcache)

