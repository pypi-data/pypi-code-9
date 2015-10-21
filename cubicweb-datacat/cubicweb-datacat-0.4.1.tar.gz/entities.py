# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-datacat entity's classes"""

from subprocess import Popen, PIPE, list2cmdline
import sys

from cubicweb import Binary
from cubicweb.predicates import has_related_entities, is_instance
from cubicweb.entities import AnyEntity, adapters
from cubicweb.view import EntityAdapter

from cubes.datacat import (register_catalog_rdf_mapping, register_dataset_rdf_mapping,
                           register_distribution_rdf_mapping, register_publisher_rdf_mapping,
                           register_contact_point_rdf_mapping)
from cubes.skos.entities import AbstractRDFAdapter


_ = unicode


def process_type_from_etype(etype):
    """Return the type of data process from etype name"""
    return etype[len('Data'):-len('Process')].lower()


def fspath_from_eid(cnx, eid):
    """Return fspath for an entity with `data` attribute stored in BFSS"""
    rset = cnx.execute('Any fspath(D) WHERE X data D, X eid %(feid)s',
                       {'feid': eid})
    if not rset:
        raise Exception('Could not find file system path for #%d.' % eid)
    return rset[0][0].read()


class Agent(AnyEntity):
    __regid__ = 'Agent'

    def dc_title(self):
        """Return a dc_title built from name and email"""
        title = self.name
        if self.email:
            title += ' <%s>' % self.email
        return title


class Dataset(AnyEntity):
    __regid__ = 'Dataset'

    def dc_title(self):
        """dc_title is either the title or the identifier"""
        return self.title or self.identifier

    @property
    def contact_point(self):
        """Contact point of this Dataset"""
        if self.dataset_contact_point:
            return self.dataset_contact_point[0]


class Distribution(AnyEntity):
    __regid__ = 'Distribution'

    def dc_title(self):
        """dc_title is either the title or the identifier"""
        return self.title or u'{0} #{1}'.format(self.cw_etype, self.eid)


class DownloadableDistribution(adapters.IDownloadableAdapter):
    """IDownloadable adapter for Distribution entities related to a File."""

    __select__ = (adapters.IDownloadableAdapter.__select__ &
                  has_related_entities('file_distribution', role='object'))

    @property
    def downloadable_file(self):
        """The IDownloadable adapted distribution file."""
        dfile = self.entity.reverse_file_distribution[0]
        return dfile.cw_adapt_to('IDownloadable')

    def download_url(self, **kwargs):
        return self.downloadable_file.download_url(**kwargs)

    def download_content_type(self):
        return self.downloadable_file.download_content_type()

    def download_encoding(self):
        return self.downloadable_file.download_encoding()

    def download_file_name(self):
        return self.downloadable_file.download_file_name()

    def download_data(self):
        return self.downloadable_file.download_data()


class ResourceFeed(AnyEntity):
    __regid__ = 'ResourceFeed'

    @property
    def dataset(self):
        """The Dataset using this ResourceFeed."""
        return self.resource_feed_of[0]

    def scripts_pending_transformation_of(self, inputfile):
        """Yield transformation scripts which have not transformed specified
        `inputfile`.
        """
        rset = self._cw.execute(
            'Any S WHERE RF transformation_script S, RF eid %(rf)s, '
            'NOT EXISTS(TP process_script S, TP process_input_file F, F eid %(f)s, '
            '           X produced_by TP)',
            {'f': inputfile.eid, 'rf': self.eid})
        return rset.entities()

    def scripts_pending_validation_of(self, inputfile):
        """Return the validation script if it has not validated specified
        `inputfile` yet.
        """
        rset = self._cw.execute(
            'Any S WHERE RF validation_script S, RF eid %(rf)s, F eid %(f)s,'
            '            NOT EXISTS(F validated_by VP, VP process_script S)',
            {'f': inputfile.eid, 'rf': self.eid})
        if rset:
            # Cardinality is "?".
            return rset.one()

    def add_transformation_process(self, inputfile, script=None,
                                   depends_on=None):
        """Add a transformation process for `inputfile` using `script`"""
        script = script or self.transformation_script[0]
        if script is None:
            return
        return self._add_process(inputfile, script, 'transformation',
                                 process_depends_on=depends_on)

    def add_validation_process(self, inputfile, script=None):
        """Add a validation process for `inputfile`"""
        script = script or self.validation_script[0]
        if script is None:
            return
        return self._add_process(inputfile, script, 'validation')

    def _add_process(self, inputfile, script, ptype, **kwargs):
        """Launch a script of type `ptype` with `inputfile`"""
        process = self._cw.create_entity(
            'Data%sProcess' % ptype.capitalize(),
            process_for_resourcefeed=self, process_script=script, **kwargs)
        self.info('created %s for resource feed #%d', process, self.eid)
        iprocess = process.cw_adapt_to('IDataProcess')
        # Adding the input file to data process triggers the "start"
        # transition.
        iprocess.add_input(inputfile)
        return process


#
# Adapters
#

# Export to RDF

class DataCatalogRDFAdapter(AbstractRDFAdapter):
    """Adapt DataCatalog entities to RDF using DCAT vocabulary."""
    __regid__ = 'RDFPrimary'
    __select__ = AbstractRDFAdapter.__select__ & is_instance('DataCatalog')

    register_rdf_mapping = staticmethod(register_catalog_rdf_mapping)

    def fill(self, graph):
        super(DataCatalogRDFAdapter, self).fill(graph)
        reg = self.registry
        reg.register_prefix('foaf', 'http://xmlns.com/foaf/0.1/')
        catalog_uri = graph.uri(self.entity.absolute_url())
        # Export license attribute as an RDF resource
        if self.entity.license:
            graph.add(catalog_uri,
                      graph.uri(reg.normalize_uri('dcterms:license')),
                      graph.uri(self.entity.license))
        # Export homepage attribute as an RDF resource
        if self.entity.homepage:
            graph.add(catalog_uri,
                      graph.uri(reg.normalize_uri('foaf:homepage')),
                      graph.uri(self.entity.homepage))
        # Export language
        lang = self.entity._cw.property_value('ui.language')
        graph.add(catalog_uri,
                  graph.uri(reg.normalize_uri('dcterms:language')),
                  graph.uri(u'http://lexvo.org/id/iso639-1/{0}'.format(lang)))


class DatasetRDFAdapter(AbstractRDFAdapter):
    """Adapt Dataset entities to RDF using DCAT vocabulary."""
    __regid__ = 'RDFPrimary'
    __select__ = AbstractRDFAdapter.__select__ & is_instance('Dataset')

    register_rdf_mapping = staticmethod(register_dataset_rdf_mapping)

    def fill(self, graph):
        super(DatasetRDFAdapter, self).fill(graph)
        reg = self.registry
        dataset_uri = graph.uri(self.entity.absolute_url())
        # Export comma-separated keyword attribute as multiple RDF resources
        if self.entity.keyword:
            for keyword in self.entity.keyword.split(u','):
                graph.add(dataset_uri,
                          graph.uri(reg.normalize_uri('dcat:keyword')),
                          keyword.strip())


class DistributionRDFAdapter(AbstractRDFAdapter):
    """Adapt Distribution entities to RDF using DCAT vocabulary."""
    __regid__ = 'RDFPrimary'
    __select__ = AbstractRDFAdapter.__select__ & is_instance('Distribution')

    register_rdf_mapping = staticmethod(register_distribution_rdf_mapping)

    def fill(self, graph):
        super(DistributionRDFAdapter, self).fill(graph)
        reg = self.registry
        distribution_uri = graph.uri(self.entity.absolute_url())
        # Export access_url and download_url attributes as an RDF resource
        if self.entity.access_url:
            graph.add(distribution_uri,
                      graph.uri(reg.normalize_uri('dcat:accessURL')),
                      graph.uri(self.entity.access_url))
        if self.entity.download_url:
            graph.add(distribution_uri,
                      graph.uri(reg.normalize_uri('dcat:downloadURL')),
                      graph.uri(self.entity.download_url))
        # Export license attribute as an RDF resource
        if self.entity.licence:
            graph.add(distribution_uri,
                      graph.uri(reg.normalize_uri('dcterms:license')),
                      graph.uri(self.entity.licence))
        # Export format attribute as an RDF resource
        if self.entity.format:
            graph.add(distribution_uri,
                      graph.uri(reg.normalize_uri('dcterms:format')),
                      graph.uri(self.entity.format))


class AgentRDFAdapter(AbstractRDFAdapter):
    """Adapt Agent entities to foaf:Agent RDF using FOAF vocabulary."""
    __regid__ = 'RDFPrimary'
    __select__ = AbstractRDFAdapter.__select__ & has_related_entities('dataset_publisher', 'object')

    register_rdf_mapping = staticmethod(register_publisher_rdf_mapping)

    def fill(self, graph):
        super(AgentRDFAdapter, self).fill(graph)
        reg = self.registry
        # Export dcat_type attribute as an RDF resource
        reg.register_prefix('dcterms', 'http://purl.org/dc/terms/')
        if self.entity.dcat_type:
            graph.add(graph.uri(self.entity.absolute_url()),
                      graph.uri(reg.normalize_uri('dcterms:type')),
                      graph.uri(self.entity.dcat_type))
        self.fill_email(graph)

    def fill_email(self, graph):
        reg = self.registry
        # Export email attribute as a owl:Thing RDF resource
        reg.register_prefix('foaf', 'http://xmlns.com/foaf/0.1/')
        if self.entity.email:
            graph.add(graph.uri(self.entity.absolute_url()),
                      graph.uri(reg.normalize_uri('foaf:mbox')),
                      graph.uri(u'mailto:{0}'.format(self.entity.email)))


class ContactPointRDFAdapter(AgentRDFAdapter):
    """Adapt Agent entities to vcard:Kind RDF using vCard vocabulary."""
    __regid__ = 'RDFContactPoint'
    __select__ = AbstractRDFAdapter.__select__ & has_related_entities('dataset_contact_point',
                                                                      'object')

    register_rdf_mapping = staticmethod(register_contact_point_rdf_mapping)

    def fill_email(self, graph):
        reg = self.registry
        # Export email attribute as a owl:Thing RDF resource
        reg.register_prefix('vcard', 'http://www.w3.org/2006/vcard/ns#')
        if self.entity.email:
            graph.add(graph.uri(self.entity.absolute_url()),
                      graph.uri(reg.normalize_uri('vcard:hasEmail')),
                      graph.uri(u'mailto:{0}'.format(self.entity.email)))


# Other adapters

class DataProcessAdapter(EntityAdapter):
    """Interface for data processes"""
    __regid__ = 'IDataProcess'
    __select__ = (EntityAdapter.__select__ &
                  is_instance('DataTransformationProcess',
                              'DataValidationProcess'))

    @property
    def process_type(self):
        """The type of data process"""
        return process_type_from_etype(self.entity.cw_etype)

    def state_name(self, name):
        """Return the full workflow state name given a short name"""
        wfs = 'wfs_dataprocess_' + name
        wf = self.entity.cw_adapt_to('IWorkflowable').current_workflow
        if wf.state_by_name(wfs) is None:
            raise ValueError('invalid state name "%s"' % name)
        return wfs

    def tr_name(self, name):
        """Return the full workflow transition name given a short name"""
        wft = 'wft_dataprocess_' + name
        wf = self.entity.cw_adapt_to('IWorkflowable').current_workflow
        if wf.transition_by_name(wft) is None:
            raise ValueError('invalid transition name "%s"' % name)
        return wft

    def fire_workflow_transition(self, trname, **kwargs):
        """Fire transition identified by *short* name `trname` of the
        underlying workflowable entity.
        """
        tr = self.tr_name(trname)
        iwf = self.entity.cw_adapt_to('IWorkflowable')
        return iwf.fire_transition(tr, **kwargs)

    @property
    def process_script(self):
        """The process script attached to entity"""
        if self.entity.process_script:
            assert len(self.entity.process_script) == 1  # schema
            return self.entity.process_script[0]

    def add_input(self, inputfile):
        """Add an input file to the underlying data process"""
        self.entity.cw_set(process_input_file=inputfile)

    def build_output(self, inputfile, data, **kwargs):
        """Return an ouput File produced from `inputfile` with `data` as
        content.
        """
        return self._cw.create_entity('File', data=Binary(data),
                                      data_name=inputfile.data_name,
                                      data_format=inputfile.data_format,
                                      produced_by=self.entity, **kwargs)

    def execute_script(self, inputfile):
        """Execute script in a subprocess using ``inputfile``.

        Eventually set process output file and return subprocess return
        code and subprocess stderr.
        """
        datapath = fspath_from_eid(self._cw, inputfile.eid)
        script = self.process_script
        scriptpath = fspath_from_eid(self._cw, script.implemented_by[0].eid)
        cmdline = [sys.executable, scriptpath, datapath]
        proc = Popen(cmdline, stdout=PIPE, stderr=PIPE)
        self.info('starting subprocess with pid %s: %s',
                  proc.pid, list2cmdline(cmdline))
        stdoutdata, stderrdata = proc.communicate()
        if proc.returncode:
            self.info('subprocess terminated abnormally (exit code %d)',
                      proc.returncode)
        if self.process_type == 'transformation':
            if stdoutdata:
                feid = self.build_output(inputfile, stdoutdata).eid
                self.info(
                    'created File #%d from input file #%d and script #%d',
                    feid, inputfile.eid, self.process_script.eid)
            else:
                # XXX raise?
                self.info('no standard output produced by Script #%d',
                          script.eid)
        return proc.returncode, unicode(stderrdata, errors='ignore')

    def finalize(self, returncode,  stderr):
        """Finalize a data process firing the proper transition."""
        if returncode:
            self.fire_workflow_transition('error', comment=stderr)
        else:
            self.fire_workflow_transition('complete', comment=stderr)
