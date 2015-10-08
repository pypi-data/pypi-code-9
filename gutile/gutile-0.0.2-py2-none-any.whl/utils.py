#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-10-08 15:02:52
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-10-08 15:40:38

from oauth2client import file, client, tools


def get_credentials(client_secret_file, default_token, scopes):
    """
    FIXME DOCs
    Taken from:
    https://developers.google.com/drive/web/quickstart/python
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(
            parents=[tools.argparser]).parse_known_args()[0]
    except ImportError:
        flags = None
        logr.error(
            'Unable to parse oauth2client args; `pip install argparse`')

    store = file.Storage(default_token)

    credentials = store.get()
    if not credentials or credentials.invalid:

        flow = client.flow_from_clientsecrets(
            client_secret_file, scopes)
        flow.redirect_uri = client.OOB_CALLBACK_URN
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        # logr.info('Storing credentials to ' + default_token)

    return credentials
