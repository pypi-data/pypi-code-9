# copyright 2014-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-datacat server objects"""

import hashlib

from cubicweb.dataimport import RQLObjectStore
from cubes.datacat.dataimport import fetch_rdf_dcat_ext_entities, import_dcat_ext_entities

from cubicweb import Binary
from cubicweb.server.sources import datafeed


class DCATFeedParser(datafeed.DataFeedParser):
    """Parse an RDF data feed with DCAT vocabulary."""

    __regid__ = 'rdf.dcat'

    def process(self, url, raise_on_error=False):
        """Import external entities from a RDF DCAT source given by its URL.

        This parser use an RQLObjectStore to import ext entities with all constraints checking.

        If raise_on_error is True, raise an exception if something goes wrong during import. False
        by default, that is: errors are logged but passed silently.
        """
        dcat_meta_uri = 'http://www.w3.org/ns/dcat.ttl'
        # Fetch ext entities from RDF DCAT source
        ext_entities = fetch_rdf_dcat_ext_entities(url, self._cw.vreg.schema, dcat_meta_uri,
                                                   import_log=self.import_log,
                                                   raise_on_error=raise_on_error)
        # Import external entities into actual CubicWeb entities using RQLObjectStore
        store = RQLObjectStore(cnx=self._cw)
        created, updated = import_dcat_ext_entities(ext_entities, store, self._cw,
                                                    source=self.source,
                                                    import_log=self.import_log,
                                                    raise_on_error=raise_on_error)
        self.stats['created'] = created
        self.stats['updated'] = updated
        # XXX: dataimport have to be modified, so that import_entities also return an error if a
        # problem occured during import.
        return False


class ResourceFeedParser(datafeed.DataFeedParser):
    """Fetch files and apply validation and transformation processes before
    attaching them to their Dataset as Resources.
    """
    __regid__ = 'datacat.resourcefeed-parser'

    def process(self, url, raise_on_error=False):
        """Build a File entity from data fetched from url"""
        stream = self.retrieve_url(url)
        data = stream.read()
        extid = self.compute_extid(data)
        # File's attributes.
        attributes = {'data_name': url.split('/')[-1],
                      'data': Binary(data)}
        entity = self.extid2entity(extid, 'File', fileattrs=attributes)
        # Launch validation and transformation scripts of all related
        # ResourceFeed entities.
        assert self.source.eid is not None
        cwsource = self._cw.entity_from_eid(self.source.eid)
        data_format = None
        for resourcefeed in cwsource.reverse_resource_feed_source:
            if data_format:
                # XXX Better do this in a schema constraint on
                # `resource_feed_source` relation.
                if resourcefeed.data_format != data_format:
                    raise ValueError('MIME types of resource feeds attached to '
                                     'CWSource #%d mismatch' % cwsource.eid)
            else:
                data_format = resourcefeed.data_format
                entity.cw_set(data_format=resourcefeed.data_format,
                              file_distribution=resourcefeed.resourcefeed_distribution)
            # Link imported file to distribution.
            self._cw.execute(
                'SET F file_distribution D WHERE F eid %(f)s, R resourcefeed_distribution D, '
                'R eid %(r)s, NOT EXISTS(F file_distribution D)',
                {'f': entity.eid, 'r': resourcefeed.eid})
            # Run the validation script for imported file.
            vscript = resourcefeed.scripts_pending_validation_of(entity)
            vprocess = None
            if vscript:
                vprocess = resourcefeed.add_validation_process(
                    entity, script=vscript)
            # Run transformation scripts that did not operate on imported file
            # already.
            for script in resourcefeed.scripts_pending_transformation_of(entity):
                resourcefeed.add_transformation_process(entity, script=script,
                                                        depends_on=vprocess)

    def before_entity_copy(self, entity, sourceparams):
        """Complete File entity with attributes"""
        entity.cw_edited.update(sourceparams['fileattrs'])

    @staticmethod
    def compute_extid(value):
        """Compute an extid based on the SHA1 hex digest computation,
        similarly to File entities"""
        return unicode(hashlib.sha1(value).hexdigest())
