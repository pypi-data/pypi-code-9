# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-datacat views/forms/actions/components for web ui"""

from cubicweb.predicates import has_related_entities, is_instance
from cubicweb.view import EntityView
from cubicweb.web import component
from cubicweb.web.views import uicfg, ibreadcrumbs, tabs, tableview

_ = unicode

abaa = uicfg.actionbox_appearsin_addmenu
afs = uicfg.autoform_section
affk = uicfg.autoform_field_kwargs
pvds = uicfg.primaryview_display_ctrl
pvs = uicfg.primaryview_section

# File
pvs.tag_subject_of(('File', 'file_distribution', '*'), 'attributes')
#afs.tag_subject_of(('File', 'resource_of', '*'), 'main', 'hidden')
afs.tag_object_of(('*', 'process_input_file', 'File'), 'main', 'hidden')


class ScriptImplementationBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    """Define Script / <Implementation> breadcrumbs"""
    __select__ = (ibreadcrumbs.IBreadCrumbsAdapter.__select__ &
                  has_related_entities('implemented_by', role='object') &
                  # Prevent select ambiguity ad File can be object of both
                  # `implemented_by` and `file_distribution` relations.
                  ~has_related_entities('file_distribution', role='subject'))

    def parent_entity(self):
        return self.entity.reverse_implemented_by[0]


class DistributionFileBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    """Define Distribution / File breadcrumbs"""
    __select__ = (ibreadcrumbs.IBreadCrumbsAdapter.__select__ &
                  has_related_entities('file_distribution', role='subject'))

    def parent_entity(self):
        return self.entity.file_distribution[0]


# Dataset
afs.tag_subject_of(('Dataset', 'dataset_publisher', '*'), 'main', 'inlined')
afs.tag_subject_of(('Dataset', 'dataset_distribution', '*'), 'main', 'inlined')
afs.tag_subject_of(('Dataset', 'dataset_contact_point', '*'), 'main', 'inlined')


class DistributionBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    """Define Dataset / Distribution breadcrumbs"""
    __select__ = (ibreadcrumbs.IBreadCrumbsAdapter.__select__ &
                  has_related_entities('of_dataset', role='subject'))

    def parent_entity(self):
        return self.entity.of_dataset[0]


class DatasetTabbedPrimaryView(tabs.TabbedPrimaryView):
    """Tabs for Dataset primary view"""
    __select__ = tabs.TabbedPrimaryView.__select__ & is_instance('Dataset')
    tabs = tabs.TabbedPrimaryView.tabs + [_('datacat.dataset_distributions_tab')]


pvs.tag_object_of(('*', 'of_dataset', 'Dataset'), 'hidden')


class DatasetDistributionsTab(tabs.TabsMixin, EntityView):
    """Tab for Dataset's distributions"""
    __regid__ = 'datacat.dataset_distributions_tab'
    __select__ = EntityView.__select__ & has_related_entities('of_dataset', role='object')

    def entity_call(self, entity):
        rset = entity.related('of_dataset', role='object')
        self._cw.view('datacat.distribution-table', rset=rset, w=self.w)


# Distribution

class DistributionTableView(tableview.EntityTableView):
    """Table view for Distribution entities"""
    __regid__ = 'datacat.distribution-table'
    __select__ = tableview.EntityTableView.__select__ & is_instance('Distribution')
    columns = ['entity', 'access_url', 'licence',
               'file_distribution_object', 'format']

    def get_latest_file(dist):
        """Return the most recent file associated to a Distribution entity."""
        rset = dist._cw.execute(
            'Any F,MD ORDERBY MD DESC LIMIT 1 WHERE F file_distribution D,'
            '                                       F modification_date MD,'
            '                                       D eid %(eid)s',
            {'eid': dist.eid})
        return rset.get_entity(0, 0) if rset else None

    column_renderers = {
        'entity': tableview.MainEntityColRenderer(),
        'file_distribution_object': tableview.RelatedEntityColRenderer(get_latest_file),
    }


pvs.tag_object_of(('*', 'resourcefeed_distribution', 'Distribution'), 'attributes')
pvs.tag_object_of(('*', 'file_distribution', 'Distribution'), 'hidden')

class DistributionFileCtxComponent(component.EntityCtxComponent):
    """Display resource files in Dataset primary view"""
    __regid__ = 'datacat.distribution-files'
    __select__ = (component.EntityCtxComponent.__select__ &
                  is_instance('Distribution') &
                  has_related_entities('file_distribution', role='object'))
    title = _('file_distribution_object')
    context = 'navcontentbottom'

    def render_body(self, w):
        rset = self._cw.execute(
            'Any F,O,S,CD WHERE F file_distribution X, F produced_by S?, '
            'F produced_from O?, F creation_date CD, X eid %(eid)s',
            {'eid': self.entity.eid})
        w(self._cw.view('table', rset=rset))


# ResourceFeed
for rtype in ('transformation_script', 'validation_script'):
    pvs.tag_subject_of(('ResourceFeed', rtype, '*'), 'attributes')
pvs.tag_object_of(('*', 'process_for_resourcefeed', 'ResourceFeed'), 'hidden')
afs.tag_subject_of(('ResourceFeed', 'resource_feed_source', '*'),
                   'main', 'hidden')
for rtype in ('transformation_script', 'validation_script'):
    afs.tag_subject_of(('ResourceFeed', rtype, '*'),
                       'main', 'attributes')
    abaa.tag_subject_of(('ResourceFeed', rtype, '*'), True)
abaa.tag_object_of(('*', 'process_for_resourcefeed', 'ResourceFeed'), False)


class ResourceFeedBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    """Define Dataset / ResourceFeed breadcrumbs"""
    __select__ = (ibreadcrumbs.IBreadCrumbsAdapter.__select__ &
                  has_related_entities('resource_feed_of', role='subject'))

    def parent_entity(self):
        """The Dataset"""
        return self.entity.resource_feed_of[0]


class DataProcessInResourceFeedCtxComponent(component.EntityCtxComponent):
    """Display data processes in ResourceFeed primary view"""
    __regid__ = 'datacat.resourcefeed-dataprocess'
    __select__ = (component.EntityCtxComponent.__select__ &
                  is_instance('ResourceFeed') &
                  has_related_entities('process_for_resourcefeed',
                                       role='object'))
    title = _('Data processes')
    context = 'navcontentbottom'

    def render_body(self, w):
        rset = self._cw.execute(
            'Any P,I,S,D WHERE P process_for_resourcefeed X,'
            '                  P process_input_file I,'
            '                  P in_state ST, ST name S,'
            '                  D? process_depends_on P,'
            '                  X eid %(eid)s',
            {'eid': self.entity.eid})
        if rset:
            w(self._cw.view('table', rset=rset))
        rset = self._cw.execute(
            'Any P,I,S,D WHERE P process_for_resourcefeed X,'
            '                  P process_input_file I,'
            '                  P in_state ST, ST name S,'
            '                  P process_depends_on D?,'
            '                  X eid %(eid)s',
            {'eid': self.entity.eid})
        if rset:
            w(self._cw.view('table', rset=rset))


# Script
afs.tag_object_of(('*', 'process_script', 'Script'),
                  'main', 'hidden')
afs.tag_subject_of(('Script', 'implemented_by', '*'), 'main', 'inlined')
pvs.tag_attribute(('Script', 'name'), 'hidden')


# DataTransformationProcess, DataValidationProcess
for etype in ('DataTransformationProcess', 'DataValidationProcess'):
    afs.tag_subject_of((etype, 'process_input_file', '*'),
                       'main', 'attributes')
    pvs.tag_subject_of((etype, 'process_input_file', '*'), 'attributes')
    affk.set_fields_order(etype, ('name', 'description',
                                  ('process_input_file', 'subject')))
