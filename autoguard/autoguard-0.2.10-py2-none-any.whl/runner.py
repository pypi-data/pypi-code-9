# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS.
# This code is distributed under the two-clause BSD License.

import os.path

from sentry.utils.runner import run_app, initialize_app


def main():
    here = os.path.dirname(__file__)
    run_app(
        project='autoguard',
        default_config_path=os.path.join(here, 'sentry_conf.py'),
        default_settings='autoguard.sentry_conf',
        settings_envvar='SENTRY_CONF',
        initializer=initialize_app,
    )

if __name__ == '__main__':
    main()
