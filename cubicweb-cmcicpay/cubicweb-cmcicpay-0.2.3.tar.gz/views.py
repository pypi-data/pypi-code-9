# copyright 2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-cmcicpay views/forms/actions/components for web ui"""

import os

from cubicweb import ValidationError
from cubicweb.web import controller
from cubicweb.predicates import match_user_groups
from cubicweb.view import StartupView
from cubicweb.web.views.urlrewrite import SimpleReqRewriter, rgx

from cubes.cmcicpay import cmcic

def get_tpe(_cw):
    return cmcic.get_tpe(os.path.join(_cw.vreg.config.apphome,'tpe'))

def traceback_as_str():
    from StringIO import StringIO
    import traceback
    out = StringIO()
    traceback.print_exc(file=out)
    return out.getvalue()

## urls

class ConfRewrite(SimpleReqRewriter):
    rules = [
        (rgx('/cmcic_info'), dict(vid='cmcic_info')),
        ]

## views

class CmcicInfoView(StartupView):
    __regid__ = 'cmcic_info'
    title = _('CMCIC paiement')
    __select__ = StartupView.__select__ & match_user_groups('managers')

    def call(self):
        self.w(u'<h1>CM-CIC p@iement</h1>')
        tpe = get_tpe(self._cw)
        self.w(u'<table>')
        for attr in ['version','tpe_number','tpe_company','server_url','return_url']:
            self.w(u'<tr><td>%s</td><td>%s</td></tr>' % (attr, getattr(tpe, attr)))
        self.w(u'</table>')

# handle callback from payment server

from cubicweb.server.repository import Repository
from logilab.common.decorators import monkeypatch

@monkeypatch(Repository)
def shopcart_checkout(self, eid, comment):
    session = self.internal_session()
    try:
        cart = session.entity_from_eid(eid)
        cart.fire_transition('check out', comment=comment)
        session.commit()
    finally:
        session.close()

class CmcicController(controller.Controller):
    __regid__ = 'cmcic'

    def publish(self, rset=None):
        self._cw.set_content_type('text/plain')
        self._cw.set_header('Pragma', 'no-cache')
        tpe = get_tpe(self._cw)
        try:
            ack = self.handle_msg(tpe)
        except Exception, exc:
            self.error(traceback_as_str())
            self.error('form data was: %s' % repr(self._cw.form))
            ack = 1
        ret = 'version=2\ncdr=%s' % ack
        self.info('cmcic returning %s' % repr(ret))
        return ret


    def handle_msg(self, tpe):
        params = dict(self._cw.form)
        self.info('cmcic handle_msg, params=%s' % repr(params))
        rep = tpe.read_paymentresponse(params)
        msg, mac = tpe.paymentresponse_msg(rep)
        if tpe.is_valid_msg(msg, mac):
            self.info('cmcic received valid message %s %s' % (repr(rep.reference), repr(rep.return_code)))
            if rep.return_code == "Annulation":
                # Payment was rejected
                # The payment may be accepted later
                return 0

            elif rep.return_code in ("payetest", "paiement"):
                # Payment was accepted
                comment = u'payed by %(brand)s on %(date)s, auth %(numauto)s' % rep.as_dict()
                try:
                    self.appli.repo.shopcart_checkout(int(rep.reference), comment)
                    return 0
                except ValidationError, exc:
                    self.error(traceback_as_str())
                    return 1

            #*** ONLY FOR MULTIPART PAYMENT ***#
            elif rep.return_code.startswith("paiement_pf"):
                # Payment part #N was accepted
                # return code is paiement_pf[#N], amount in Rpeification['montantech']
                pass

            elif rep.return_code.startswith("Annulation_pf"):
                # Payment part #N was rejected
                # return code is Annulation_pf[#N], amount in Repification['montantech']
                pass
        else:
            self.warning("cmcic received invalid message %s %s" % (repr(rep.reference), repr(rep.return_code)))
        return 1
