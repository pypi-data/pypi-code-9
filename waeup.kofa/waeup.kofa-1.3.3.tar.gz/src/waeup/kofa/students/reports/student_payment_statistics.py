## $Id: student_payment_statistics.py 12897 2015-05-01 14:32:09Z henrik $
##
## Copyright (C) 2015 Uli Fouquet & Henrik Bettermann
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
import grok
from zope.i18n import translate
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility
from zope.interface import implementer, Interface, Attribute
from waeup.kofa.interfaces import (
    IKofaUtils,
    academic_sessions_vocab, registration_states_vocab)
from waeup.kofa.students.vocabularies import StudyLevelSource
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.reports import IReport


class IStudentPaymentStatisticsReport(IReport):

    session = Attribute('Session to report')
    mode = Attribute('Study modes group to report')
    level = Attribute('Level to report')
    creation_dt_string = Attribute('Human readable report creation datetime')


def get_student_payment_stats(session, mode, level, breakdown):
    """Get payment amounts of students in a certain session, study mode
    and current level.

    Returns a table ordered by code (faculty or department, one per row) and
    various payment categories (cols). The result is a 3-tuple representing
    ((<CODES>), (<PAYMENTCATS>), (<NUM_OF_STUDENTS>)). The
    (<NUM_OF_STUDENTS>) is an n-tuple with each entry containing the
    number of students found in that faculty/department and with the respective
    payment.

    Sample result:

      >>> ((u'FAC1', u'FAC2'),
      ...  ('clearance', 'gown', 'hostel_maintenance', 'schoolfee'),
      ...  ((12, 10, 1, 14), (0, 5, 25, 16)))

    This result means: there are 5 students in FAC2 in who have paid
    gown fee while 12 students in 'FAC1' who have paid for clearance.
    """
    site = grok.getSite()
    payment_cats_dict = getUtility(IKofaUtils).REPORTABLE_PAYMENT_CATEGORIES
    payment_cats = tuple(sorted(payment_cats_dict.keys())) + ('Total',)
    if breakdown == 'faccode':
        codes = tuple(sorted([x for x in site['faculties'].keys()],
                                 key=lambda x: x.lower()))
        paths = codes
    elif breakdown == 'depcode':
        faculties = site['faculties']
        depcodes = []
        deppaths = []
        for fac in faculties.values():
            for dep in fac.values():
                depcodes.append(dep.code)
                deppaths.append('%s/%s' % (fac.code, dep.code))
        codes = tuple(sorted([x for x in depcodes],
                                 key=lambda x: x.lower()))
        paths = tuple(sorted([x for x in deppaths],
                                 key=lambda x: x.lower()))
    # XXX: Here we do _one_ query and then examine the single
    #   students. One could also do multiple queries and just look for
    #   the result length (not introspecting the delivered students
    #   further).
    cat = queryUtility(ICatalog, name="students_catalog")
    result = cat.searchResults(current_session=(session, session))
    table = [[0 for x in xrange(2*len(payment_cats))] for y in xrange(len(codes)+1)]
    mode_groups = getUtility(IKofaUtils).MODE_GROUPS
    for stud in result:
        if mode != 'All' and stud.current_mode not in mode_groups[mode]:
            continue
        if level != 0 and stud.current_level != level:
            continue
        if getattr(stud, breakdown) not in codes:
            # studs can have a faccode ``None``
            continue
        row = codes.index(getattr(stud, breakdown))
        for key in stud['payments'].keys():
            ticket = stud['payments'][key]
            if ticket.p_category not in payment_cats or\
                ticket.p_state != 'paid' or\
                ticket.p_session != session:
                continue
            col = payment_cats.index(ticket.p_category)

            # payments in category and fac/dep
            table[row][2*col] += 1 # number of payments
            table[row][2*col+1] += ticket.amount_auth

            # payments in category
            table[-1][2*col] += 1
            table[-1][2*col+1] += ticket.amount_auth

            # payments in fac/dep
            table[row][-2] += 1
            table[row][-1] += ticket.amount_auth

            # all payments
            table[-1][-2] += 1
            table[-1][-1] += ticket.amount_auth

    # Build table header
    table_header = ['' for x in xrange(len(payment_cats))]
    for cat in payment_cats:
        cat_title = payment_cats_dict.get(cat, cat)
        table_header[payment_cats.index(cat)] = cat_title

    # Turn lists into tuples
    table = tuple([tuple(row) for row in table])

    paths = paths + (u'Total',)
    return (paths, table_header, table)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Table, Spacer
from waeup.kofa.reports import IReport, IReportGenerator
from waeup.kofa.reports import Report
from waeup.kofa.browser.interfaces import IPDFCreator
from waeup.kofa.students.reports.level_report import TTR

from waeup.kofa.students.reports.student_statistics import (
    tbl_data_to_table, STYLE)

def tbl_data_to_table(row_names, col_names, data):
    result = []
    new_col_names = []
    for name in col_names:
        if len(name) > 18:
            new_col_names.append(name.replace(' ', '\n', 1))
        else:
            new_col_names.append(name)
    head = [''] + [col_name for col_name in new_col_names]
    result = [head]
    for idx, row_name in enumerate(row_names):
        row = []
        i = 0
        while i < len(data[idx]):
            row.append("%s (%s)" % ("{:,}".format(data[idx][i+1]), data[idx][i]))
            i += 2
        row = [row_name] + row
        result.append(row)
    return result

TABLE_STYLE = [
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8),
    ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 8),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8),
    ('FONT', (0,-1), (-1,-1), 'Helvetica-Bold', 8),
    ('FONT', (-1,0), (-1,-1), 'Helvetica-Bold', 8),
    ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black),
    ('LINEAFTER', (-1,0), (-1,-1), 0.25, colors.black),
    ('LINEBEFORE', (-1,0), (-1,-1), 0.25, colors.black),
    #('LINEABOVE', (0,-1), (-1,-1), 1.0, colors.black),
    #('LINEABOVE', (0,0), (-1,0), 0.25, colors.black),
    ]

@implementer(IStudentPaymentStatisticsReport)
class StudentPaymentStatisticsReport(Report):
    data = None
    session = None
    mode = None

    def __init__(self, session, mode, level, breakdown, author='System'):
        super(StudentPaymentStatisticsReport, self).__init__(
            args=[session, mode, breakdown], kwargs={'author':author})
        self.studylevelsource = StudyLevelSource().factory
        self.portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.session = academic_sessions_vocab.getTerm(session).title
        self.mode = mode
        if level == 0:
            self.level = ''
        else:
            self.level = translate(self.studylevelsource.getTitle(None, int(level)),
                'waeup.kofa', target_language=self.portal_language)
        self.breakdown = breakdown
        self.author = author
        self.creation_dt_string = self.creation_dt.astimezone(
            getUtility(IKofaUtils).tzinfo).strftime("%Y-%m-%d %H:%M:%S %Z")
        self.data = get_student_payment_stats(session, mode, level, breakdown)

    def create_pdf(self):
        creator = getUtility(IPDFCreator, name='landscape')
        table_data = tbl_data_to_table(*self.data)
        col_widths = [None,] + [3.2*cm] * len(self.data[1]) + [None,]
        pdf_data = [Paragraph('<b>%s</b>' % self.creation_dt_string,
                              STYLE["Normal"]),
                    Spacer(1, 12),]
        pdf_data += [
            Table(table_data, style=TABLE_STYLE, colWidths=col_widths)]
        if not self.level:
            doc_title = translate(
                _('${a} Student Payments - ${b}',
                mapping = {'a':self.mode, 'b':self.session}))
            pdf = creator.create_pdf(
                pdf_data, None, doc_title, self.author, doc_title + '-'
                )
        else:
            doc_title = translate(
                _('${a} Student Payments - ${b} - ${c}',
                mapping = {'a':self.mode, 'b': self.level, 'c':self.session}))
            pdf = creator.create_pdf(
                pdf_data, None, doc_title, self.author, doc_title + '-'
                )
        return pdf


@implementer(IReportGenerator)
class StudentPaymentStatisticsReportGenerator(grok.GlobalUtility):

    title = _('Student Payment Statistics')
    grok.name('student_payment_stats')

    def generate(
        self, site, session=None, mode=None,
        level=None, breakdown=None, author=None):
        result = StudentPaymentStatisticsReport(
            session=session, mode=mode, level=level,
            breakdown=breakdown, author=author)
        return result

###############################################################
## Browser related stuff
##
## XXX: move to local browser module
###############################################################
from waeup.kofa.browser.layout import KofaPage
from waeup.kofa.interfaces import academic_sessions_vocab
from waeup.kofa.reports import get_generators
from waeup.kofa.browser.breadcrumbs import Breadcrumb
grok.templatedir('browser_templates')

from waeup.kofa.students.reports.student_statistics import (
    StudentStatisticsReportGeneratorPage,
    StudentStatisticsReportPDFView)

class StudentPaymentStatisticsReportGeneratorPage(
    StudentStatisticsReportGeneratorPage):

    grok.context(StudentPaymentStatisticsReportGenerator)
    grok.template('studentstatisticsreportgeneratorpage')

    label = _('Create student payment statistics report')


class StudentPaymentStatisticsReportPDFView(StudentStatisticsReportPDFView):

    grok.context(IStudentPaymentStatisticsReport)

    def _filename(self):
        return 'StudentPaymentStatisticsReport_%s_%s_%s_%s.pdf' % (
            self.context.session, self.context.mode, self.context.level,
            self.context.creation_dt_string)


class StudentStatsBreadcrumb(Breadcrumb):
    """A breadcrumb for reports.
    """
    grok.context(StudentPaymentStatisticsReportGenerator)
    title = _(u'Student Payment Statistics')
    target = None