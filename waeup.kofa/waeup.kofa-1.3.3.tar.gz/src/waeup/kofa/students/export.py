## $Id: export.py 13281 2015-10-05 09:40:36Z henrik $
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
"""Exporters for student related stuff.
"""
import os
import grok
from datetime import datetime, timedelta
from zope.component import getUtility
from waeup.kofa.interfaces import (
    IExtFileStore, IFileStoreNameChooser, IKofaUtils)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.students.catalog import StudentsQuery, CourseTicketsQuery
from waeup.kofa.students.interfaces import (
    IStudent, IStudentStudyCourse, IStudentStudyLevel, ICourseTicket,
    IStudentOnlinePayment, ICSVStudentExporter, IBedTicket)
from waeup.kofa.students.vocabularies import study_levels
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names, to_timezone


def get_students(site, stud_filter=StudentsQuery()):
    """Get all students registered in catalog in `site`.
    """
    return stud_filter.query()

def get_studycourses(students):
    """Get studycourses of `students`.
    """
    return [x.get('studycourse', None) for x in students
            if x is not None]

def get_levels(students):
    """Get all studylevels of `students`.
    """
    levels = []
    for course in get_studycourses(students):
        for level in course.values():
            levels.append(level)
    return levels

def get_tickets(students, **kw):
    """Get course tickets of `students`.
    If code is passed through, filter course tickets
    which belong to this course code and meets level
    and level_session.
    """
    tickets = []
    code = kw.get('code', None)
    level = kw.get('level', None)
    level_session = kw.get('session', None)
    if code is None:
        for level_obj in get_levels(students):
            for ticket in level_obj.values():
                tickets.append(ticket)
    else:
        for level_obj in get_levels(students):
            for ticket in level_obj.values():
                if ticket.code != code:
                    continue
                if level is not None:
                    level = int(level)
                    if level_obj.level in (10, 999, None)  \
                        and int(level) != level_obj.level:
                        continue
                    if level_obj.level not in range(level, level+100, 10):
                        continue
                if level_session is not None and \
                    int(level_session) != level_obj.level_session:
                    continue
                tickets.append(ticket)
    return tickets

def get_payments(students, p_state=None, **kw):
    """Get all payments of `students` within given payment_date period.
    """
    date_format = '%d/%m/%Y'
    payments = []
    payments_start = kw.get('payments_start')
    payments_end = kw.get('payments_end')
    if payments_start and payments_end:
        # Payment period given
        payments_start = datetime.strptime(payments_start, date_format)
        payments_end = datetime.strptime(payments_end, date_format)
        tz = getUtility(IKofaUtils).tzinfo
        payments_start = tz.localize(payments_start)
        payments_end = tz.localize(payments_end) + timedelta(days=1)
        if p_state:
            # Only paid or unpaid tickets in payment period are considered
            for student in students:
                for payment in student.get('payments', {}).values():
                    if payment.payment_date and payment.p_state == p_state:
                        payment_date = to_timezone(payment.payment_date, tz)
                        if payment_date > payments_start and \
                            payment_date < payments_end:
                            payments.append(payment)
        else:
            # All tickets in payment period are considered
            for student in students:
                for payment in student.get('payments', {}).values():
                    if payment.payment_date:
                        payment_date = to_timezone(payment.payment_date, tz)
                        if payment_date > payments_start and \
                            payment_date < payments_end:
                            payments.append(payment)
    else:
        # Payment period not given
        if p_state:
            # Only paid tickets are considered
            for student in students:
                for payment in student.get('payments', {}).values():
                    if payment.p_state == p_state:
                        payments.append(payment)
        else:
            # All tickets are considered
            for student in students:
                for payment in student.get('payments', {}).values():
                    payments.append(payment)
    return payments

def get_bedtickets(students):
    """Get all bedtickets of `students`.
    """
    tickets = []
    for student in students:
        for ticket in student.get('accommodation', {}).values():
            tickets.append(ticket)
    return tickets

class StudentExporterBase(ExporterBase):
    """Exporter for students or related objects.
    This is a baseclass.
    """
    grok.baseclass()
    grok.implements(ICSVStudentExporter)
    grok.provides(ICSVStudentExporter)

    def filter_func(self, x, **kw):
        return x

    def get_filtered(self, site, **kw):
        """Get students from a catalog filtered by keywords.
        students_catalog is the default catalog. The keys must be valid
        catalog index names.
        Returns a simple empty list, a list with `Student`
        objects or a catalog result set with `Student`
        objects.

        .. seealso:: `waeup.kofa.students.catalog.StudentsCatalog`

        """
        # Pass only given keywords to create FilteredCatalogQuery objects.
        # This way we avoid
        # trouble with `None` value ambivalences and queries are also
        # faster (normally less indexes to ask). Drawback is, that
        # developers must look into catalog to see what keywords are
        # valid.
        if kw.get('catalog', None) == 'coursetickets':
            coursetickets = CourseTicketsQuery(**kw).query()
            students = []
            for ticket in coursetickets:
                students.append(ticket.student)
            return list(set(students))
        # Payments can be filtered by payment_date. The period boundaries
        # are not keys of the catalog and must thus be removed from kw.
        try:
            del kw['payments_start']
            del kw['payments_end']
        except KeyError:
            pass
        query = StudentsQuery(**kw)
        return query.query()

    def get_selected(self, site, selected):
        """Get set of selected students.
        Returns a simple empty list or a list with `Student`
        objects.
        """
        students = []
        students_container = site.get('students', {})
        for id in selected:
            student = students_container.get(id, None)
            if student:
                students.append(student)
        return students

    def export(self, values, filepath=None):
        """Export `values`, an iterable, as CSV file.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for value in values:
            self.write_item(value, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export students into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        return self.export(self.filter_func(get_students(site)), filepath)

    def export_student(self, student, filepath=None):
        return self.export(self.filter_func([student]), filepath=filepath)

    def export_filtered(self, site, filepath=None, **kw):
        """Export items denoted by `kw`.
        If `filepath` is ``None``, a raw string with CSV data should
        be returned.
        """
        data = self.get_filtered(site, **kw)
        return self.export(self.filter_func(data, **kw), filepath=filepath)

    def export_selected(self,site, filepath=None, **kw):
        """Export data for selected set of students.
        """
        selected = kw.get('selected', [])
        data = self.get_selected(site, selected)
        return self.export(self.filter_func(data, **kw), filepath=filepath)


class StudentExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Exporter first filters the set of students by searching the
    students catalog. Then it exports student base data of this set of students.
    """
    grok.name('students')

    fields = tuple(sorted(iface_names(IStudent))) + (
        'password', 'state', 'history', 'certcode', 'is_postgrad',
        'current_level', 'current_session')
    title = _(u'Students')

    def mangle_value(self, value, name, context=None):
        """The mangler prepares the history messages and adds a hash symbol at
        the end of the phone number to avoid annoying automatic number
        transformation by Excel or Calc."""
        if name == 'history':
            value = value.messages
        if name == 'phone' and value is not None:
            # Append hash '#' to phone numbers to circumvent
            # unwanted excel automatic
            value = str('%s#' % value)
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)


class StudentStudyCourseExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Study Course Exporter first filters the set of students
    by searching the students catalog. Then it exports the data of the current
    study course container of each student from this set. It does
    not export their content.
    """
    grok.name('studentstudycourses')

    fields = tuple(sorted(iface_names(IStudentStudyCourse))) + ('student_id',)
    title = _(u'Student Study Courses')

    def filter_func(self, x, **kw):
        return get_studycourses(x)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the certificate code and the student id.
        """
        if name == 'certificate' and value is not None:
            # XXX: hopefully cert codes are unique site-wide
            value = value.code
        if name == 'student_id' and context is not None:
            student = context.student
            value = getattr(student, name, None)
        return super(
            StudentStudyCourseExporter, self).mangle_value(
            value, name, context=context)


class StudentStudyLevelExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Study Level Exporter first filters the set of students
    by searching the students catalog. Then it exports the data of the student's
    study level container data but not their content (course tickets).
    The exporter iterates over all objects in the students' ``studycourse``
    containers.
    """
    grok.name('studentstudylevels')

    fields = tuple(sorted(iface_names(
        IStudentStudyLevel))) + (
        'student_id', 'number_of_tickets','certcode')
    title = _(u'Student Study Levels')

    def filter_func(self, x, **kw):
        return get_levels(x)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student id, nothing else.
        """
        if name == 'student_id' and context is not None:
            student = context.student
            value = getattr(student, name, None)
        return super(
            StudentStudyLevelExporter, self).mangle_value(
            value, name, context=context)

class CourseTicketExporter(grok.GlobalUtility, StudentExporterBase):
    """The Course Ticket Exporter exports course tickets. Usually,
    the exporter first filters the set of students by searching the
    students catalog. Then it collects and iterates over all ``studylevel``
    containers of the filtered student set and finally
    iterates over all items inside these containers.

    If the course code is passed through, the exporter uses a different
    catalog. It searches for students in the course tickets catalog and
    exports those course tickets which belong to the given course code and
    also meet level and session passed through at the same time.
    This happens if the exporter is called at course level in the academic
    section.
    """
    grok.name('coursetickets')

    fields = tuple(sorted(iface_names(ICourseTicket) +
        ['level', 'code', 'level_session'])) + ('student_id',
        'certcode', 'display_fullname')
    title = _(u'Course Tickets')

    def filter_func(self, x, **kw):
        return get_tickets(x, **kw)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id and fullname.
        """
        if context is not None:
            student = context.student
            if name in ('student_id', 'display_fullname') and student is not None:
                value = getattr(student, name, None)
        return super(
            CourseTicketExporter, self).mangle_value(
            value, name, context=context)


class StudentPaymentExporter(grok.GlobalUtility, StudentExporterBase):
    """The Student Payment Exporter first filters the set of students
    by searching the students catalog. Then it exports student payment
    tickets by iterating over the items of the student's ``payments``
    container. If the payment period is given only tickets, which were
    paid in payment period, are considered for export.
    """
    grok.name('studentpayments')

    fields = tuple(
        sorted(iface_names(
            IStudentOnlinePayment, exclude_attribs=False,
            omit=['display_item']))) + (
            'student_id','state','current_session')
    title = _(u'Student Payments')

    def filter_func(self, x, **kw):
        return get_payments(x, **kw)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student's id, registration
        state and current session.
        """
        if context is not None:
            student = context.student
            if name in ['student_id','state',
                        'current_session'] and student is not None:
                value = getattr(student, name, None)
        return super(
            StudentPaymentExporter, self).mangle_value(
            value, name, context=context)

class StudentUnpaidPaymentExporter(StudentPaymentExporter):
    """The Student Unpaid Payment Exporter works just like the
    Student Payments Exporter but it exports only unpaid tickets.
    This exporter is designed for finding and finally purging outdated
    payment ticket.
    """
    grok.name('studentunpaidpayments')

    title = _(u'Student Unpaid Payments')

    def filter_func(self, x, **kw):
        return get_payments(x, p_state='unpaid', **kw)

class DataForBursaryExporter(StudentPaymentExporter):
    """The DataForBursary Exporter works just like the Student Payments Exporter
    but it exports much more information about the student. It combines
    payment and student data in one table in order to spare postprocessing of 
    two seperate export files. The exporter is primarily used by bursary
    officers who have exclusively access to this exporter.
    """
    grok.name('bursary')

    def filter_func(self, x, **kw):
        return get_payments(x, p_state='paid', **kw)

    fields = tuple(
        sorted(iface_names(
            IStudentOnlinePayment, exclude_attribs=False,
            omit=['display_item']))) + (
            'student_id','matric_number','reg_number',
            'firstname', 'middlename', 'lastname',
            'state','current_session',
            'entry_session', 'entry_mode',
            'faccode', 'depcode','certcode')
    title = _(u'Payment Data for Bursary')

    def mangle_value(self, value, name, context=None):
        """The mangler fetches the student data.
        """
        if context is not None:
            student = context.student
            if name in [
                'student_id','matric_number', 'reg_number',
                'firstname', 'middlename', 'lastname',
                'state', 'current_session',
                'entry_session', 'entry_mode',
                'faccode', 'depcode', 'certcode'] and student is not None:
                value = getattr(student, name, None)
        return super(
            StudentPaymentExporter, self).mangle_value(
            value, name, context=context)

class BedTicketExporter(grok.GlobalUtility, StudentExporterBase):
    """The Bed Ticket Exporter first filters the set of students
    by searching the students catalog. Then it exports bed
    tickets by iterating over the items of the student's ``accommodation``
    container.
    """
    grok.name('bedtickets')

    fields = tuple(
        sorted(iface_names(
            IBedTicket, exclude_attribs=False,
            omit=['display_coordinates']))) + (
            'student_id', 'actual_bed_type')
    title = _(u'Bed Tickets')

    def filter_func(self, x, **kw):
        return get_bedtickets(x)

    def mangle_value(self, value, name, context=None):
        """The mangler determines the student id and the type of the bed
        which has been booked in the ticket.
        """
        if context is not None:
            student = context.student
            if name in ['student_id'] and student is not None:
                value = getattr(student, name, None)
        if name == 'bed' and value is not None:
            value = getattr(value, 'bed_id', None)
        if name == 'actual_bed_type':
            value = getattr(getattr(context, 'bed', None), 'bed_type')
        return super(
            BedTicketExporter, self).mangle_value(
            value, name, context=context)

class StudentPaymentsOverviewExporter(StudentExporter):
    """The Student Payments Overview Exporter first filters the set of students
    by searching the students catalog. Then it exports some student base data
    together with the total school fee amount paid in each year over a
    predefined year range (current year - 9, ... , current year + 1).
    """
    grok.name('paymentsoverview')

    curr_year = datetime.now().year
    year_range = range(curr_year - 9, curr_year + 1)
    year_range_tuple = tuple([str(year) for year in year_range])

    fields = ('student_id', 'matric_number', 'display_fullname',
        'state', 'certcode', 'faccode', 'depcode', 'is_postgrad',
        'current_level', 'current_session', 'current_mode', 'entry_session'
        ) + year_range_tuple
    title = _(u'Student Payments Overview')

    def mangle_value(self, value, name, context=None):
        """The mangler summarizes the school fee amounts made per year. It
        iterates over all paid school fee payment tickets and
        adds together the amounts paid in a year. Waived payments
        are marked ``waived``.
        """
        if name in self.year_range_tuple and context is not None:
            value = 0
            for ticket in context['payments'].values():
                if ticket.p_category == 'schoolfee' and \
                    ticket.p_session == int(name):
                    if ticket.p_state == 'waived':
                        value = 'waived'
                        break
                    if ticket.p_state == 'paid':
                        try:
                            value += ticket.amount_auth
                        except TypeError:
                            pass
            if value == 0:
                value = ''
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)

class StudentStudyLevelsOverviewExporter(StudentExporter):
    """The Student Study Levels Overview Exporter first filters the set of
    students by searching the students catalog. Then it exports some student
    base data together with the session key of registered levels.
    Sample output:

    header: ``...100,110,120,200,210,220,300...``

    data: ``...2010,,,2011,2012,,2013...``

    This csv data string means that level 100 was registered in session 
    2010/2011, level 200 in session 2011/2012, level 210 (200 on 1st probation)
    in session 2012/2013 and level 300 in session 2013/2014.
    """
    grok.name('studylevelsoverview')

    avail_levels = tuple([str(x) for x in study_levels(None)])

    fields = ('student_id', ) + (
        'state', 'certcode', 'faccode', 'depcode', 'is_postgrad',
        'entry_session', 'current_level', 'current_session',
        ) + avail_levels
    title = _(u'Student Study Levels Overview')

    def mangle_value(self, value, name, context=None):
        """The mangler checks if a given level has been registered. It returns
        the ``level_session`` attribute of the student study level object
        if the named level exists.
        """
        if name in self.avail_levels and context is not None:
            value = ''
            for level in context['studycourse'].values():
                if level.level == int(name):
                    value = '%s' % level.level_session
                    break
        return super(
            StudentExporter, self).mangle_value(
            value, name, context=context)

class ComboCardDataExporter(grok.GlobalUtility, StudentExporterBase):
    """Like all other exporters the Combo Card Data Exporter first filters the
    set of students by searching the students catalog. Then it exports some
    student base data which are neccessary to print for the Interswitch combo 
    card (identity card for students). The output contains a ``passport_path``
    column which contains the filesystem path of the passport image file.
    If no path is given, no passport image file exists.
    """
    grok.name('combocard')

    fields = ('display_fullname',
              'student_id','matric_number',
              'certificate', 'faculty', 'department', 'passport_path')
    title = _(u'Combo Card Data')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the titles of faculty, department
        and certificate. It also computes the path of passport image file
        stored in the filesystem.
        """
        certificate = context['studycourse'].certificate
        if name == 'certificate' and certificate is not None:
            value = certificate.title
        if name == 'department' and certificate is not None:
            value = certificate.__parent__.__parent__.longtitle
        if name == 'faculty' and certificate is not None:
            value = certificate.__parent__.__parent__.__parent__.longtitle
        if name == 'passport_path' and certificate is not None:
            file_id = IFileStoreNameChooser(context).chooseName(
                attr='passport.jpg')
            os_path = getUtility(IExtFileStore)._pathFromFileID(file_id)
            if not os.path.exists(os_path):
                value = None
            else:
                value = '/'.join(os_path.split('/')[-4:])
        return super(
            ComboCardDataExporter, self).mangle_value(
            value, name, context=context)