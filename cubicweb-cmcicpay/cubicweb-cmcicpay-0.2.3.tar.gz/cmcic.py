#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
=======================================
Python module to handle CM-CIC p@iement
=======================================

Config file
============

Config file must look like:

[cmcic_tpe]
number: 0123456
key: 0123456789012345678901234567890123456789
version: 3.0
company: acme
server_url = http://paymentserver.com/paiement.cgi
return_url = http://merchant.com/cmcic

Submit payment
==============

Example of code that generates the html page with the form that links to the
payment server.

.. sourcecode:: python

    import cmcic

    # initialize terminal
    tpe = cmcic.get_tpe('mytpe')

    # build payment request
    payreq = cmcic.PaymentRequest()
    payreq.reference = "ref" + datetime.datetime.now().strftime("%H%M%S");
    payreq.amount = "1.01"
    payreq.currency = "EUR"
    payreq.description = "Some description"
    payreq.date = datetime.datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
    payreq.lang = "FR"
    payreq.email = "test@test.zz"
    payreq.url_root = 'http://www.toto.com/'
    payreq.url_ok = 'http://www.toto.com/cart/1234'
    payreq.url_err = 'http://www.toto.com/cart/1234'

    # generate html
    print '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">
    <head>
    <title>Test serveur de paiement CMCIC</title>
    </head>

    <body>
    <h1>Test serveur de paiement CMCIC</h1>

    <p>Identification du terminal <pre>%s</pre></p>
    <p>Sceau MAC <pre>%s</pre></p>
    %s
    </body>
    </html>
    ''' % (tpe.id_str(),
           tpe.paymentrequest_msg(payreq)[1],
           cmcic.html_form(tpe, payreq))

Acknowledge payment
===================

Example of code that handles the response from the payment server and
acknowledges that response upon reception.

.. sourcecode:: python

    import cmcic

    # initialize terminal
    tpe = cmcic.get_tpe('mytpe')

    # handle response
    payrep = tpe.read_paymentresponse(cgi.FieldStorage())
    msg, mac = tpe.paymentresponse_msg(payrep)
    if tpe.is_valid_msg(msg, mac):
        if payrep.return_code == "Annulation":
            # Payment has been refused
            # The payment may be accepted later
            pass

        elif payrep.return_code in ("payetest","paiement"):
            # Payment has been accepeted on the productive server
            pass

        #*** ONLY FOR MULTIPART PAYMENT ***#
        elif payrep.return_code.startswith("paiement_pf"):
            # Payment has been accepted on the productive server for the part #N
            # return code is like paiement_pf[#N]
            # put your code here (email sending / Database update)
            # You have the amount of the payment part in Certification['montantech']
            pass

        elif payrep.return_code.startswith("Annulation_pf"):
            # Payment has been refused on the productive server for the part #N
            # return code is like Annulation_pf[#N]
            # put your code here (email sending / Database update)
            # You have the amount of the payment part in Certification['montantech']
            pass

        sResult = "0"
    else :
        # your code if the HMAC doesn't match
        sResult = "1\n" + mac

    #-----------------------------------------------------------------------------
    # Send receipt to CMCIC server
    #-----------------------------------------------------------------------------
    print "Pragma: no-cache\nContent-type: text/plain\n\nversion=2\ncdr=" + sResult

"""
__docformat__ = 'restructuredtext'

import hmac, hashlib, os.path, ConfigParser

def dict_translate(msg, map):
    result = {}
    for key, value in msg.items():
        key = map.get(key, key)
        if key is not None:
            result[key] = value
    return result

class NamedTuple(object):
    __slots__ = ()

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.pop(attr, None))
        if kwargs:
            raise NameError('No attributes named %s' % repr(kwargs))

    def as_dict(self):
        result = {}
        for attr in self.__slots__:
            result[attr] = getattr(self, attr)
        return result

class PaymentRequest(NamedTuple):
    """
    reference  : unique, alphaNum (A-Z a-z 0-9), 12 characters max
    amount     : format  "xxxxx.yy" (no spaces)
    currency   : ISO 4217 compliant
    description: session context for the return on the merchant website
    date       : format dd/mm/yyyy:hh:mm:ss
    email      : buyer's email
    payments   : amount must be paid in at most 4 payments [(date1, amount1), ...]
    options    : ...
    """
    __slots__ = ('mac reference amount currency description date email payments '
                 'options url_root url_ok url_err lang').split()

class PaymentResponse(NamedTuple):
    __slots__ = ('mac reference amount date description return_code cvx vld '
                 'brand status3ds numauto motifrefus originecb bincb hpancb '
                 'ipclient originetr veres pares montantech').split()

# same order as in CM-CIC_paiement_documentation_technique_v3_0.pdf
RESPONSE_TRANSLATION = dict([
    ('MAC','mac'), ('TPE', None), ('montant','amount'), ('texte-libre','description'),
    ('code-retour','return_code'),
    ])

REQUEST_TRANSLATION = dict([
    ('version', None), ('TPE', None), ('montant', 'amount'),
    ('texte-libre', 'description'), ('mail', 'email'),
    ('lgue','lang'), ('societe', None), ('url_retour', 'url_root'),
    ('url_retour_ok', 'url_ok'), ('url_retour_err', 'url_err'),
    ('MAC','mac'), ('bouton', None),
    ])

class PaymentProtocol(object):

    def __init__(self, cfg) :
        self.version = cfg.get('cmcic_tpe', 'version')
        self.tpe_key = self.decode_key(cfg.get('cmcic_tpe', 'key'))
        self.tpe_number = cfg.get('cmcic_tpe', 'number')
        self.tpe_company = cfg.get('cmcic_tpe', 'company')
        self.server_url = cfg.get('cmcic_tpe', 'server_url')
        self.return_url = cfg.get('cmcic_tpe', 'return_url')

    def decode_key(self, key):
        hexStrKey = key[0:38]
        hexFinal = key[38:40] + "00"
        cca0 = ord(hexFinal[0:1])
        if cca0 > 70 and cca0 < 97:
            hexStrKey += chr(cca0-23) + hexFinal[1:2]
        elif hexFinal[1:2] == "M":
            hexStrKey += hexFinal[0:1] + "0"
        else:
            hexStrKey += hexFinal[0:2]
        import encodings.hex_codec
        c = encodings.hex_codec.Codec()
        hexStrKey = c.decode(hexStrKey)[0]
        return hexStrKey

    def compute_hmac(self, data):
        hash = hmac.HMAC(self.tpe_key, None, hashlib.sha1)
        hash.update(data)
        return hash.hexdigest()

    def id_str(self):
        msg = "CtlHmac%s%s" % (self.version, self.tpe_number)
        return "V1.04.sha1.py--[%s]-%s" % (msg, self.compute_hmac(msg))

    def read_paymentrequest(self, params):
        params = dict_translate(params, REQUEST_TRANSLATION)
        req = PaymentRequest(**params)
        return req

    def read_paymentresponse(self, params):
        params = dict_translate(params, RESPONSE_TRANSLATION)
        req = PaymentResponse(**params)
        return req

    def paymentrequest_msg(self, req):
        items = [self.tpe_number, req.date, req.amount+req.currency,
                 req.reference, req.description, self.version,
                 req.lang, self.tpe_company, req.email]
        payments = req.payments or []
        if len(payments):
            items.append(len(payments))
        else:
            items.append('')
        for date, amount in payments:
            items.append(date)
            items.append(amount+req.currency)
        for i in range(len(payments),4):
            items.append('')
            items.append('')
        items.append(req.options or '')
        items = [str(item) for item in items]
        msg = '*'.join(items)
        hmac = self.compute_hmac(msg)
        return msg, hmac

    def paymentresponse_msg(self, rep):
        items = []
        for item in [self.tpe_number, rep.date, rep.amount, rep.reference, rep.description,
                     rep.return_code, rep.cvx, rep.vld, rep.brand, rep.status3ds,
                     rep.numauto, rep.motifrefus, rep.originecb, rep.bincb, rep.hpancb,
                     rep.ipclient, rep.originetr, rep.veres, rep.pares, '']:
            if item is None:
                items.append('')
            else:
                items.append(item)
        msg = '*'.join(items)
        hmac = self.compute_hmac(msg)
        return msg, hmac

    def is_valid_msg(self, msg, mac):
        return self.compute_hmac(msg) == mac.lower()

# by default submit = u'<input type="submit" name="bouton" id="bouton" value="%s" />' % label

def html_form(tpe, req, submit):
    form = [u'<form action="%s" method="post" id="PaymentRequest">' % tpe.server_url]
    msg, mac = tpe.paymentrequest_msg(req)
    fields = [("version"         ,tpe.version),
              ("TPE"             ,tpe.tpe_number),
              ("date"            ,req.date),
              ("montant"         ,req.amount + req.currency),
              ("reference"       ,req.reference),
              ("MAC"             ,mac),
              ("url_retour"      ,req.url_root),
              ("url_retour_ok"   ,req.url_ok),
              ("url_retour_err"  ,req.url_err),
              ("lgue"            ,req.lang),
              ("societe"         ,tpe.tpe_company),
              ("texte-libre"     ,req.description),
              ("mail"            ,req.email),
              ]
    for name, value in fields:
	form.append(u'<input type="hidden" name="%s" id="%s" value="%s" />' % (name, name, value))
    form.append(submit)
    form.append(u'</form>')
    return u''.join(form)

def get_tpe(cfgpath):
    cfg = ConfigParser.RawConfigParser()
    cfg.read(cfgpath)
    return PaymentProtocol(cfg)

