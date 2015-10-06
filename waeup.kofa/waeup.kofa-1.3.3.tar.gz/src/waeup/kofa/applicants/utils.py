## $Id: utils.py 13216 2015-08-24 05:56:39Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""General helper functions and utilities for the applicants section.
"""

from time import time
import grok
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.applicants.interfaces import IApplicantsUtils
from waeup.kofa.applicants.workflow import (INITIALIZED,
    STARTED, PAID, ADMITTED, NOT_ADMITTED, SUBMITTED, CREATED)

class ApplicantsUtils(grok.GlobalUtility):
    """A collection of parameters and methods subject to customization.
    """
    grok.implements(IApplicantsUtils)

    #: A dictionary containing application type names, titles and
    #: access code prefixes (meanwhile deprecated).
    APP_TYPES_DICT = {
      'app': ['General Studies', 'APP'],
      'special': ['Special Application', 'SPE'],
      }

    #: A dictionary which maps widget names to headlines.
    #: The headline is rendered in forms and on pdf slips above the
    #: respective display or input widget.
    SEPARATORS_DICT = {
      'form.course1': _(u'Desired Study Courses'),
      'form.student_id': _(u'Process Data'),
      }

    def setPaymentDetails(self, container, payment, applicant):
        """Set the payment data of an applicant.
        In contrast to its `StudentsUtils` counterpart, the payment ticket
        must exist and is an argument of this method.
        """
        timestamp = ("%d" % int(time()*10000))[1:]
        session = str(container.year)
        try:
            session_config = grok.getSite()['configuration'][session]
        except KeyError:
            return _(u'Session configuration object is not available.')
        payment.p_id = "p%s" % timestamp
        payment.p_item = container.title
        payment.p_session = container.year
        payment.amount_auth = 0.0
        if applicant.special:
            if applicant.special_application:
                fee_name = applicant.special_application + '_fee'
                payment.amount_auth = getattr(session_config, fee_name, None)
                if payment.amount_auth in (0.0, None):
                    return _('Amount could not be determined.')
                payment.p_category = applicant.special_application
            return
        payment.p_category = 'application'
        container_fee = container.application_fee
        if container_fee:
            payment.amount_auth = container_fee
            return
        payment.amount_auth = session_config.application_fee
        if payment.amount_auth in (0.0, None):
            return _('Amount could not be determined.')
        return

    def getApplicantsStatistics(self, container):
        """Count applicants in applicants containers.
        """
        state_stats = {INITIALIZED:0, STARTED:0, PAID:0, SUBMITTED:0,
            ADMITTED:0, NOT_ADMITTED:0, CREATED:0}
        cat = getUtility(ICatalog, name='applicants_catalog')
        code = container.code
        for state in state_stats:
            if state == 'initialized':
                results = cat.searchResults(
                                state=(state, state),
                                container_code=(code + '+', code + '+'))
                state_stats[state] = len(results)
            else:
                results = cat.searchResults(
                    state=(state, state),
                    container_code=(code + '+', code + '-'))
                state_stats[state] = len(results)
        return state_stats, None

    def sortCertificates(self, context, resultset):
        """Sort already filtered certificates in `AppCatCertificateSource`.
        Display also current course even if certificate in the academic
        section has been removed.
        """
        resultlist = sorted(resultset, key=lambda value: value.code)
        curr_course = context.course1
        if curr_course is not None and curr_course not in resultlist:
            resultlist = [curr_course,] + resultlist
        return resultlist

    def getCertTitle(self, context, value):
        """Compose the titles in `AppCatCertificateSource`.
        """
        return "%s - %s" % (value.code, value.title)
