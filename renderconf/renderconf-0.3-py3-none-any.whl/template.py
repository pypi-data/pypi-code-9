# -*- coding: utf-8 -*-
import jinja2
import logging
import os

log = logging.getLogger(__name__)


class RenderError(Exception):
    pass


def render(template_dir, context, target_root=''):
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        undefined=jinja2.StrictUndefined,
    )
    for template_name in environment.list_templates():
        if os.path.basename(template_name).startswith('.'):
            continue
        log.info('Rendering template {}'.format(template_name))
        target = os.path.join(target_root, template_name)
        if os.path.dirname(target):
            os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'w') as f:
            try:
                f.write(environment.get_template(template_name).render(context))
            except jinja2.exceptions.UndefinedError as e:
                raise RenderError(
                    'Missing variable in template {}: {}'.format(template_name, e)
                )
