## $Id: export.py 13216 2015-08-24 05:56:39Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
"""Exporters for applicant-related stuff.
"""
import grok
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from waeup.kofa.applicants.interfaces import (
    IApplicantBaseData, IApplicantsContainer)
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.batching import ExporterBase
from waeup.kofa.utils.helpers import iface_names

class ApplicantsContainerExporter(grok.GlobalUtility, ExporterBase):
    """The Applicants Container Exporter exports container data. It does not
    export applicants (application records) inside the container.
    """
    grok.implements(ICSVExporter)
    grok.name('applicantscontainers')

    fields = tuple(sorted(iface_names(IApplicantsContainer)))
    title = _(u'Applicants Containers')

    def mangle_value(self, value, name, context=None):
        return super(
            ApplicantsContainerExporter, self).mangle_value(
            value, name, context=context)

    def export(self, containers, filepath=None):
        """Export `containers`, an iterable, as CSV file.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for container in containers:
            self.write_item(container, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export applicantscontainer into filepath as CSV data.

        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        containers = site.get('applicants', {})
        return self.export(containers.values(), filepath)


class ApplicantExporter(grok.GlobalUtility, ExporterBase):
    """The Applicant Exporter exports application records (= applicants)
    stored in the database. In contrast to the exporters in the academic
    section this exporter does not iterate over the items of containers
    but searches the :class:`ApplicantsCatalog` instead.

    The exporter exports all applicants if started in the Data Center
    which means in the context of the `DataCenter` object. The exporter can also 
    be started 'locally' which means in the context of an `ApplicantsContainer`
    container. Then the :meth:`export_filtered()` instead of the 
    :meth:`export_all()` method is applied which searches for applicants
    in the respective container.
    """
    grok.implements(ICSVExporter)
    grok.name('applicants')

    fields = tuple(sorted(iface_names(IApplicantBaseData))) + (
        'password', 'state', 'history', 'container_code', 'application_number',
        'display_fullname', 'application_date')
    title = _(u'Applicants')

    def mangle_value(self, value, name, context=None):
        """The mangler determines the codes of the atributes `course1`,
        `course2` and `course_admitted`. It furthermore prepares the
        history messages and adds a hash symbol at the end of the phone number
        to avoid annoying automatic number transformation by Excel or Calc.
        """
        if name in (
            'course1', 'course2', 'course_admitted') and value is not None:
            value = value.code
        #elif name == 'school_grades':
        #    value = [eval(entry.to_string()) for entry in value]
        elif name == 'history':
            value = value.messages
        elif name == 'phone' and value is not None:
            # Append hash '#' to phone numbers to circumvent
            # unwanted excel automatic
            value = str('%s#' % value)
        elif name == 'container_code':
            value = value.strip('+')
        return super(
            ApplicantExporter, self).mangle_value(
            value, name, context=context)

    def export(self, applicants, filepath=None):
        """Export `applicants`, an iterable, as CSV file.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for applicant in applicants:
            self.write_item(applicant, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export all applicants into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        Only used records are being exported.
        """
        catalog = queryUtility(
            ICatalog, context=site, name='applicants_catalog', default=None)
        if catalog is None:
            return self.export([], filepath)
        applicants = catalog.searchResults(
            # reg_num might not be set and then would not be found.
            # We therefore search for applicant_id.
            applicant_id=(None, None))
        used = [value for value in applicants if value.container_code.endswith('+')]
        return self.export(used, filepath=filepath)

    def export_filtered(self, site, filepath=None, **kw):
        """Export filtered applicants in container denoted by keywords (`kw`).
        If `filepath` is ``None``, a raw string with CSV data should
        be returned. Only used records are being exported.
        """
        container = grok.getSite()['applicants'][kw['container']]
        container_values = container.values()
        used = [value for value in container_values if value.container_code.endswith('+')]
        return self.export(used, filepath=filepath)
