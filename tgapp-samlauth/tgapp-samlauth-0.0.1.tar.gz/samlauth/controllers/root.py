# -*- coding: utf-8 -*-
"""Main Controller"""
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.metadata import create_metadata_string
from saml2.s_utils import rndstr

from tg import TGController, auth_force_login, flash, request
from tg import expose, app_globals, session, redirect, abort, config
from tg.exceptions import HTTPFound
from tg.i18n import ugettext as _

import logging
log = logging.getLogger('tgapp-samlauth')


class RootController(TGController):
    @expose()
    def login(self, **kwargs):
        sp = app_globals.samlsp

        # We authenticate against the first IdP
        idps = sp.metadata.with_descriptor("idpsso")
        if isinstance(idps, dict):
            idps = list(idps.keys())

        try:
            entity_id = idps[0]
        except IndexError:
            return abort(404, 'No Identity Provider configured for Login')

        # Picks a binding to use for sending the Request to the IDP
        _binding, destination = sp.pick_binding("single_sign_on_service",
                                                [BINDING_HTTP_REDIRECT],
                                                "idpsso",
                                                entity_id=entity_id)
        log.debug("binding: %s, destination: %s" % (_binding, destination))

        # Binding here is the response binding that is which binding the
        # IDP should use to return the response.
        acs = sp.config.getattr("endpoints", "sp")["assertion_consumer_service"]

        # just pick one
        endp, return_binding = acs[0]

        extensions = None
        req_id, req = sp.create_authn_request(destination, binding=return_binding, extensions=extensions)
        _rstate = rndstr()
        ht_args = sp.apply_binding(_binding, "%s" % req, destination,
                                   relay_state=_rstate, sigalg="")

        session['samlauth.queries'] = {req_id: 'samlauth'}
        session.save()

        log.info("Login %s" % session['samlauth.queries'])
        raise HTTPFound(headers=ht_args["headers"])

    @expose(content_type='text/xml')
    def metadata(self, **kwargs):
        sp = app_globals.samlsp
        metadata = create_metadata_string(sp.config_file, None, None,
                                          sp.config.cert_file, sp.config.key_file,
                                          None, None, None)
        return metadata

    @expose()
    def post(self, SAMLResponse=None, **kwargs):
        if not SAMLResponse:
            abort(412, 'Missing SAMLResponse')

        saml_queries = session['samlauth.queries']
        log.info("Auth %s" % session['samlauth.queries'])

        sp = app_globals.samlsp
        response = sp.parse_authn_request_response(SAMLResponse,
                                                   BINDING_HTTP_POST,
                                                   saml_queries,
                                                   {})
        log.info("AVA: %s - %s" % (response.name_id, response.ava))

        if not response.ava:
            raise ValueError('Missing authentication data, make sure samlauth.enc_key_files are properly configured')

        userid = sp.user_data_adapter(response.ava)
        if not userid:
            flash(_('Unable to find a registered user for the provided identity'), 'error')
            return redirect(request.referer or config.sa_auth['post_logout_url'])

        auth_force_login(userid)
        redirect_to = config.sa_auth['post_login_url']
        return redirect(redirect_to)