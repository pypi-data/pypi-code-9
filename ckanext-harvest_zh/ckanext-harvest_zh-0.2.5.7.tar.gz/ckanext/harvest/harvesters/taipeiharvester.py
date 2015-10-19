# -*- coding: utf8 -*-

from ckanext.harvest.model import HarvestObject
import logging
import json
import urllib2
from hashlib import sha1

from base import HarvesterBase

log = logging.getLogger(__name__)

class TaipeiHarvester(HarvesterBase):

    url = 'http://data.taipei/opendata/datalist/apiAccess?scope=datasetMetadataSearch&q=type:dataset'
    def _get_content(self, url):
        http_request = urllib2.Request(
            url = url,
        )
        try:
            http_response = urllib2.urlopen(http_request)
        except urllib2.URLError, e:
            raise ContentFetchError(
                'Could not fetch url: %s, error: %s' %
                (url, str(e))
            )
        return http_response.read()

    def info(self):
        return {
            'name': 'data_taipei',
            'title': 'Taipei CKAN',
            'description': u'台北市政府公開資料平台專用的Harvester'
        }

    def gather_stage(self, harvest_job):
        # fetch data
        try:
            raw = self._get_content(self.url)
        except ContentFetchError,e:
            self._save_gather_error('Unable to get content for URL: %s: %s' % (self.url, str(e)),harvest_job)

        content = json.loads(raw)['result']['results']

        # create harvest object
        ids = []
        for _ in content:
            id = sha1(_['id']).hexdigest()
            obj = HarvestObject(guid=id, job=harvest_job, content=json.dumps(_))
            obj.save()
            ids.append(obj.id)
        return ids

    def fetch_stage(self, harvest_object):
        return True

    def import_stage(self,harvest_object):
        if not harvest_object:
            log.error('No harvest object received')
            return False
        if harvest_object.content is None:
            self._save_object_error('Empty content for object %s' % harvest_object.id,harvest_object,'Import')
            return False
        try:
            content = json.loads(harvest_object.content)
            package_dict = {
                    'id':harvest_object.guid,
                    'owner_org':'taipei',
                    'name': "taipei-" + content['id'],
                    'title': content['title'],
                    'url': 'http://data.taipei/opendata/datalist/datasetMeta?oid='+content['id'],
                    'notes': content.get('description'),
                    'license_id': u'臺北市政府資訊開放加值應用規範',
                    'resources': [],
                    # 'tags': content.get('tag').split(',') if content.get('tag') else []
            }
            resources = content['resources']
            for resource in resources:
                package_dict['resources'].append({
                    'name':resource['resourceName'],
                    'url':'http://data.taipei/opendata/datalist/datasetMeta/download?id='+content['id']+'&rid='+resource['resourceId'],
                    'format':resource['format'],
                    'description':resource['resourceDescription']
                })

        except Exception, e:
            log.exception(e)
            self._save_object_error('%r' % e, harvest_object, 'Import')

        return self._create_or_update_package(package_dict, harvest_object)

class ContentFetchError(Exception):
    pass
