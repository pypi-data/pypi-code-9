# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2015 LSE Leading Security Experts GmbH
#
#    This file is part of LinOTP server.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@lsexperts.de
#    Contact: www.linotp.org
#    Support: www.lsexperts.de
#
"""This file file contains the Remote token class"""

import logging
import copy
import traceback


import httplib2
import urllib
try:
    import json
except ImportError:
    import simplejson as json

from linotp.lib.config import getFromConfig
from linotp.lib.util import getParam
from linotp.lib.validate import split_pin_otp
from linotp.lib.validate import check_pin

optional = True
required = False

from linotp.lib.tokenclass import TokenClass


log = logging.getLogger(__name__)

###############################################


class RemoteTokenClass(TokenClass):
    """
    The Remote token forwards an authentication request to another LinOTP
    server. The request can be forwarded to a user on the other server or to
    a serial number on the other server. The PIN can be checked on the local
    LinOTP server or on the remote server.

    Using the Remote token you can assign one physical token to many
    different users.
    """

    def __init__(self, aToken):
        """
        constructor - create a token class object with it's db token binding

        :param aToken: the db bound token
        """
        TokenClass.__init__(self, aToken)
        self.setType(u"remote")

        self.remoteServer = ""
        self.remoteLocalCheckpin = None
        self.remoteSerial = None
        self.remoteUser = None
        self.remoteRealm = None
        self.remoteResConf = None
        self.mode = ['authenticate', 'challenge']

    @classmethod
    def getClassType(cls):
        """
        return the class type identifier
        """
        return "remote"

    @classmethod
    def getClassPrefix(cls):
        """
        return the token type prefix
        """
        return "LSRE"

    @classmethod
    def getClassInfo(cls, key=None, ret='all'):
        """
        getClassInfo - returns a subtree of the token definition

        :param key: subsection identifier
        :type key: string

        :param ret: default return value, if nothing is found
        :type ret: user defined

        :return: subsection if key exists or user defined
        :rtype: s.o.

        """
        log.debug("[getClassInfo] begin. Get class render info for section: "
                  "key %r, ret %r " % (key, ret))

        res = {'type': 'remote',
               'title': 'Remote Token',
               'description': ('REMOTE token to forward the authentication'
                               ' request to another LinOTP server'),

               'init': {'page': {'html': 'remotetoken.mako',
                                 'scope': 'enroll', },
                        'title': {'html': 'remotetoken.mako',
                                  'scope': 'enroll.title', },
                        },

               'config': {'page': {'html': 'remotetoken.mako',
                                   'scope': 'config', },
                          'title': {'html': 'remotetoken.mako',
                                    'scope': 'config.title', },
                          },

               'selfservice': {},
               'policy': {},
               }

        if key is not None and key in res:
            ret = res.get(key)
        else:
            if ret == 'all':
                ret = res

        log.debug("[getClassInfo] end. Returned the configuration section: "
                  "ret %r " % (ret))
        return ret

    def update(self, param):
        """
        second phase of the init process - updates parameters

        :param param: the request parameters
        :return: - nothing -
        """

        self.remoteServer = getParam(param, "remote.server", required)
        # if another OTP length would be specified in /admin/init this would
        # be overwritten by the parent class, which is ok.
        self.setOtpLen(6)

        val = getParam(param, "remote.local_checkpin", optional)
        if val is not None:
            self.remoteLocalCheckpin = val

        val = getParam(param, "remote.serial", optional)
        if val is not None:
            self.remoteSerial = val

        val = getParam(param, "remote.user", optional)
        if val is not None:
            self.remoteUser = val

        val = getParam(param, "remote.realm", optional)
        if val is not None:
            self.remoteRealm = val

        val = getParam(param, "remote.resConf", optional)
        if val is not None:
            self.remoteResConf = val

        TokenClass.update(self, param)

        self.addToTokenInfo("remote.server", self.remoteServer)
        self.addToTokenInfo("remote.serial", self.remoteSerial)
        self.addToTokenInfo("remote.user", self.remoteUser)
        self.addToTokenInfo("remote.local_checkpin", self.remoteLocalCheckpin)
        self.addToTokenInfo("remote.realm", self.remoteRealm)
        self.addToTokenInfo("remote.resConf", self.remoteResConf)

        return

    def check_pin_local(self):
        """
        lookup if pin should be checked locally or on remote host

        :return: bool
        """
        local_check = False
        if 1 == int(self.getFromTokenInfo("remote.local_checkpin")):
            local_check = True
        log.debug(" local checking pin? %r" % local_check)

        return local_check


    def authenticate(self, passw, user, options=None):
        """
        do the authentication on base of password / otp and user and
        options, the request parameters.

        Here we contact the other LinOTP server to validate the OtpVal.

        :param passw: the password / otp
        :param user: the requesting user
        :param options: the additional request parameters

        :return: tupple of (success, otp_count - 0 or -1, reply)

        """
        log.debug("authenticate")

        res = False
        otp_counter = -1
        reply = None

        otpval = passw

        ## should we check the pin localy??
        if self.check_pin_local():
            (res, pin, otpval) = split_pin_otp(self, passw, user,
                                               options=options)

            res = TokenClass.checkPin(self, pin)
            if res is False:
                return (res, otp_counter, reply)

        (res, otp_count, reply) = self.do_request(otpval, user=user)

        return (res, otp_count, reply)

    def is_challenge_request(self, passw, user, options=None):
        """
        This method checks, if this is a request, that triggers a challenge.
        It depends on the way, the pin is checked - either locally or remote

        :param passw: password, which might be pin or pin+otp
        :type passw: string
        :param user: The user from the authentication request
        :type user: User object
        :param options: dictionary of additional request parameters
        :type options: dict

        :return: true or false
        """

        request_is_valid = False

        if self.check_pin_local():
            pin_match = check_pin(self, passw, user=user, options=options)
            if pin_match is True:
                request_is_valid = True

        return request_is_valid

    def do_request(self, passw, transactionid=None, user=None):
        """
        run the http request against the remote host

        :param passw: the password which should be checked on the remote host
        :param transactionid: provided,  if this is a challenge response
        :param user: the requesting user - used if no remote serial or remote
                     user is provided

        :return: Tuple of (success, otp_count= -1 or 0, reply=remote response)
        """
        otpval = passw.encode("utf-8")

        remoteServer = self.getFromTokenInfo("remote.server") or ""
        remoteServer = remoteServer.encode("utf-8")

        ## in preparation of the ability to reloacte linotp urls,
        ## we introduce the remote url path
        remotePath = self.getFromTokenInfo("remote.path") or ""
        remotePath = remotePath.strip().encode('utf-8')

        remoteSerial = self.getFromTokenInfo("remote.serial") or ""
        remoteSerial = remoteSerial.encode('utf-8')

        remoteUser = self.getFromTokenInfo("remote.user") or ""
        remoteUser = remoteUser.encode('utf-8')

        remoteRealm = self.getFromTokenInfo("remote.realm") or ""
        remoteRealm = remoteRealm.encode('utf-8')

        remoteResConf = self.getFromTokenInfo("remote.resConf") or ""
        remoteResConf = remoteResConf.encode('utf-8')

        ssl_verify = getFromConfig("remote.verify_ssl_certificate",
                                   False) or False

        if type(ssl_verify) in [str, unicode]:
            if ssl_verify.lower() == "true":
                ssl_verify = True
            else:
                ssl_verify = False


        ## here we also need to check for remote.user and so on....
        log.debug("[checkOtp] checking OTP len:%r remotely on server: %r,"
                  " serial: %r, user: %r" %
                  (len(otpval), remoteServer, remoteSerial, remoteUser))
        params = {}

        if len(remoteSerial) > 0:
            params['serial'] = remoteSerial
            if len(remotePath) == 0:
                remotePath = "/validate/check_s"
        elif len(remoteUser) > 0:
            params['user'] = remoteUser
            params['realm'] = remoteRealm
            params['resConf'] = remoteResConf
            if len(remotePath) == 0:
                remotePath = "/validate/check"

        else:
        ## There is no remote.serial and no remote.user, so we will
        ## try to pass the requesting user.
            if user is None:
                log.warning("FIXME: We do not know the user at the moment!")
            else:
                params['user'] = user.login
                params['realm'] = user.realm

        params['pass'] = otpval
        if transactionid is not None:
            params['state'] = transactionid

        ## use a POST request to check the token
        data = urllib.urlencode(params)
        request_url = "%s%s" % (remoteServer, remotePath)

        reply = {}
        otp_count = -1
        res = False

        try:
            ## prepare the submit and receive headers
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}

            ## submit the request
            try:
                ## is httplib compiled with ssl?
                http = httplib2.Http(disable_ssl_certificate_validation=
                                     not(ssl_verify))
            except TypeError as exx:
                ## not so on squeeze:
                ## TypeError: __init__() got an unexpected keyword argument
                ## 'disable_ssl_certificate_validation'

                log.warning("httplib2 'disable_ssl_certificate_validation' "
                            "attribute error: %r" % exx)
                ## so we run in fallback mode
                http = httplib2.Http()

            (resp, content) = http.request(request_url,
                                           method="POST",
                                           body=data,
                                           headers=headers)
            result = json.loads(content)
            log.debug(result)
            status = result['result']['status']
            log.debug(status)

            if True == status:
                if True == result['result']['value']:
                    res = True
                    otp_count = 0

            if "detail" in result:
                reply = copy.deepcopy(result["detail"])
                otp_count = -1
                res = False

        except Exception as exx:
            log.error("[do_request] [RemoteToken] Error getting response from "
                      "remote Server (%r): %r" % (request_url, exx))
            log.error("[do_request] %r" % (traceback.format_exc()))

        return (res, otp_count, reply)

    def checkResponse4Challenge(self, user, passw, options=None,
                                challenges=None):
        '''
        This method verifies if the given ``passw`` matches any
        existing ``challenge`` of the token.

        It then returns the new otp_counter of the token and the
        list of the matching challenges.

        In case of success the otp_counter needs to be >= 0.
        The matching_challenges is passed to the method
        :py:meth:`~linotp.lib.tokenclass.TokenClass.challenge_janitor`
        to clean up challenges.

        :param user: the requesting user
        :type user: User object
        :param passw: the password (pin+otp)
        :type passw: string
        :param options:  additional arguments from the request, which could
                         be token specific
        :type options: dict
        :param challenges: A sorted list of valid challenges for this token.
        :type challenges: list
        :return: tuple of (otpcounter and the list of matching challenges)

        '''
        otp_counter = -1
        transid = None
        matching_challenge = None
        reply = None

        matching_challenges = []

        if 'transactionid' in options or 'state' in options:
            ## fetch the transactionid
            transid = options.get('transactionid', options.get('state', None))

        if transid is not None:
            ## in case of a local pin check, we the transaction is a local one
            ## and we must not forward this!!
            if self.check_pin_local():
                ## check if transaction id is in list of challengens
                for challenge in challenges:
                    if challenge.transid == transid:
                        matching_challenge = challenge
                        break

                if matching_challenge is not None:
                    (res, otp_counter, reply) = \
                        self.do_request(passw, user=user)

                    ## everything is ok, we remove the challenge
                    if res is True and otp_counter >= 0:
                        matching_challenges.append(matching_challenge)

            ## in case of remote check pin, we just forward everything
            else:
                (res, otp_counter, reply) = \
                    self.do_request(passw, transactionid=transid, user=user)

        return (otp_counter, matching_challenges)

    def checkPin(self, pin, options=None):
        """
        check the pin - either remote or localy
        - in case of remote, we return true, as the
          the splitPinPass will put the passw then in the otpVal
        """
        res = True

        ## only, if pin should be checked localy
        if self.check_pin_local():
            res = TokenClass.checkPin(self, pin)

        return res

    def splitPinPass(self, passw):
        """
        Split the PIN and the OTP value.
        Only if it is locally checked and not remotely.

        :param passw: the password with pin and otp
        :return: tupple of the (success, pin and otpvalue)

        """
        res = 0

        local_check = self.check_pin_local()


        if local_check:
            (res, pin, otpval) = TokenClass.splitPinPass(self, passw)
        else:
            pin = ""
            otpval = passw

        log.debug("[splitPinPass] [remotetoken] returnung (len:%r) (len:%r)"
                  % (len(pin), len(otpval)))
        return (res, pin, otpval)

###eof#########################################################################
