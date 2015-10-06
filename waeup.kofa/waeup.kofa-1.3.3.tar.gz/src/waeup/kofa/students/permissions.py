## $Id: permissions.py 13076 2015-06-19 05:49:57Z henrik $
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
"""
Permissions for the students section.
"""
import grok

# Students section permissions

class HandleStudent(grok.Permission):
    """
    The HandleStudent permission is reserved for students.
    Students 'handle' their data. Officers 'manage' the data.
    """
    grok.name('waeup.handleStudent')

class ViewStudent(grok.Permission):
    """
    The ViewStudent permission allows to view all student data.
    """
    grok.name('waeup.viewStudent')

class ViewMyStudentDataTab(grok.Permission):
    grok.name('waeup.viewMyStudentDataTab')

class ViewStudentsContainer(grok.Permission):
    """The ViewStudentsContainer permission allows to view the students root
    container page.
    """
    grok.name('waeup.viewStudentsContainer')

class PayStudent(grok.Permission):
    """The PayStudent permission allows to add an online payment ticket and to
    manage tickets.
    """
    grok.name('waeup.payStudent')

class HandleAccommodation(grok.Permission):
    """The HandleAccommodation allows to manage bed tickets.
    """
    grok.name('waeup.handleAccommodation')

class UploadStudentFile(grok.Permission):
    """The UploadStudentFile permissions allows to upload the passport picture.
    The respective page additionally checks the state of the student.
    """
    grok.name('waeup.uploadStudentFile')

class ManageStudent(grok.Permission):
    """The ManageStudent permission allows to edit the data.
    This permission is meant for students officers.
    """
    grok.name('waeup.manageStudent')

class ClearStudent(grok.Permission):
    """The ClearStudent permission is needed to clear students
    or to reject clearance. This permission is meant for clearance officers.
    """
    grok.name('waeup.clearStudent')

class ValidateStudent(grok.Permission):
    """The ValidateStudent permission is needed to validate or reject
    course lists. This permission is not needed if users
    already have the TriggerTransition permission.
    """
    grok.name('waeup.validateStudent')

class EditStudyLevel(grok.Permission):
    """The EditStudyLevel permission is needed for editing course lists.
    Students and course advisers do have this permission.
    """
    grok.name('waeup.editStudyLevel')

class LoginAsStudent(grok.Permission):
    """The LoginAsStudent is needed to set temporary student passwords
    and login as (impersonate) students.
    """
    grok.name('waeup.loginAsStudent')

# Local role
class StudentRecordOwner(grok.Role):
    """A student 'owns' her/his student object and subobjects and
    gains permissions to handle all data, upload a passport picture,
    add payment tickets, create and edit course lists and handle accommodation.
    """
    grok.name('waeup.local.StudentRecordOwner')
    grok.title(u'Student Record Owner')
    grok.permissions('waeup.handleStudent',
                     'waeup.uploadStudentFile',
                     'waeup.viewStudent',
                     'waeup.payStudent',
                     'waeup.handleAccommodation',
                     'waeup.editStudyLevel')

# Site Roles
class StudentRole(grok.Role):
    """This role is dedicated to students only.
    It defines the permissions a student gains portal-wide.
    """
    grok.name('waeup.Student')
    grok.title(u'Student (do not assign)')
    grok.permissions('waeup.viewAcademics',
                     'waeup.viewMyStudentDataTab',
                     'waeup.Authenticated')

class StudentsOfficer(grok.Role):
    """The Students Officer is allowed to view all student data.
    """
    grok.name('waeup.StudentsOfficer')
    grok.title(u'Students Officer (view only)')
    grok.permissions('waeup.viewStudent',
                     'waeup.viewStudentsContainer')

class StudentsManager(grok.Role):
    """The Students Officer is allowed to edit all student data, to
    create payment tickets, to handle bed tickets and to upload passport
    pictures.
    """
    grok.name('waeup.StudentsManager')
    grok.title(u'Students Manager')
    grok.permissions('waeup.viewStudent',
                     'waeup.manageStudent',
                     'waeup.viewStudentsContainer',
                     'waeup.payStudent',
                     'waeup.uploadStudentFile',
                     'waeup.handleAccommodation')

class TranscriptOfficer(grok.Role):
    grok.name('waeup.TranscriptOfficer')
    grok.title(u'Transcript Officer')
    grok.permissions('waeup.viewAcademics',
                     'waeup.viewTranscript',
                     'waeup.viewStudent',
                     'waeup.viewStudentsContainer',
                     )

class StudentsClearanceOfficer(grok.Role):
    """The global StudentsClearanceOfficer role enables users to view all
    student data, to clear students and to reject clearance portal-wide.
    Usually, this role is not assigned manually.
    We are using the correspondent local role instead which assigns the
    StudentsClearanceOfficer role dynamically.
    """
    grok.name('waeup.StudentsClearanceOfficer')
    grok.title(u'Clearance Officer (all students)')
    grok.permissions('waeup.clearStudent',
                     'waeup.viewStudent')

class StudentsCourseAdviser(grok.Role):
    """The global StudentsCourseAdviser role enables users to view all
    student data, to edit, validate or reject course lists  portal-wide.
    Usually, this role is not assigned manually.
    We are using the correspondent local role instead which assigns the
    StudentsCourseAdviser role dynamically.
    """
    grok.name('waeup.StudentsCourseAdviser')
    grok.title(u'Course Adviser (all students)')
    grok.permissions('waeup.validateStudent',
                     'waeup.viewStudent',
                     'waeup.editStudyLevel')

class StudentImpersonator(grok.Role):
    """The Student Impersonator gains the LoginAsStudent permission,
    nothing else, see description above.
    """
    grok.name('waeup.StudentImpersonator')
    grok.title(u'Student Impersonator')
    grok.permissions('waeup.loginAsStudent')