class ListMixin(object):
    """
    Caution: The current pagination system will be inaccurate when new media are being added to your account!

    * A temporary work-around is to request the entirety of your request in one call (per_page=10000..)
    """
    def all(self, page=1, per_page=1000):
        """
        Returns a generator that will continue requesting new pages of resources until there are none left.
        """
        pages = page

        while page <= pages:
            resp = self._client.request_page(self.model.list_url, page, per_page)
            pages = resp['pages']

            for item in resp['items']:
                yield self.to_instance(item)

            page += 1

    def list(self, page=1, per_page=1000):
        """
        Returns a generator that only contains media from this specific page.
        """
        resp = self._client.request_page(self.model.list_url, page, per_page)
        item_list = resp['items']
        return self.to_instance(item_list)


class CreateMixin(object):

    def create(self, **data):
        resp = self._client.request_json('POST', self.model.list_url, data=data)
        return self.to_instance(resp)


class RetrieveMixin(object):

    def retrieve(self, id):
        resp = self._client.request_json('GET', self.model.instance_url(id))
        return self.to_instance(resp)


class InstanceRetrieveMixin(object):

    def retrieve(self):
        resp = self._client.request_json('GET', self.model.instance_url(self.id))
        return self.to_instance(resp)


class UpdateMixin(object):

    def update(self, id, **data):
        resp = self._client.request_json('PUT', self.model.instance_url(id), data=data)
        return self.to_instance(resp)


class InstanceUpdateMixin(object):

    def update(self, **data):
        resp = self._client.request_json('PUT', self.model.instance_url(self.id), data=data)
        return self.to_instance(resp)


class DeleteMixin(object):

    def delete(self, id):
        self._client.request('DELETE', self.model.instance_url(id))


class InstanceDeleteMixin(object):

    def delete(self):
        self._client.request('DELETE', self.model.instance_url(self.id))


class AnalyticsMixin(object):

    def analytics(self, id, fp, timeout=10):
        """
        Download the frame-level analytics CSV associated with this id and save it to fp.
        """
        return self._client.request_to_file(fp, 'GET', self.model.analytics_url(id), timeout=timeout)


class InstanceAnalyticsMixin(object):

    def analytics(self, fp, timeout=10):
        """
        Download the frame-level analytics CSV associated with this object and save it to fp.
        """
        return self._client.request_to_file(fp, 'GET', self.model.analytics_url(self.id), timeout=timeout)


class AggregatedAnalyticsMixin(object):

    def aggregated_analytics(self, id, fp, interval='summary', report='standard', gender='both', timeout=10):
        """
        Download the aggregated analytics CSV associated with this id and save it to fp.
            - interval	The time unit of aggregation: second, quarter, summary.
            - report	The report type: standard, advanced.
            - gender	Separate or combined gender rows: both, combined.
        """
        return self._client.download_aggregated_file(fp, self.model.aggregated_analytics_url(id), interval=interval,
                                                     report=report, gender=gender, timeout=timeout)


class InstanceAggregatedAnalyticsMixin(object):

    def aggregated_analytics(self, fp, interval='summary', report='standard', gender='both', timeout=10):
        """
        Download the aggregated analytics CSV associated with this instance and save it to fp.
            - interval	The time unit of aggregation: second, quarter, summary.
            - report	The report type: standard, advanced.
            - gender	Separate or combined gender rows: both, combined.
        """
        return self._client.download_aggregated_file(fp, self.model.aggregated_analytics_url(self.id),
                                                     interval=interval, report=report, gender=gender, timeout=timeout)


class MetadataCSVMixin(object):

    def metadata(self, id, fp, timeout=10):
        """
        Download the metadata CSV for this group id
        """
        url = 'analytics/groups/{}/metadata'.format(id)
        return self._client.request_to_file(fp, 'GET', url, timeout=timeout)


class InstanceMetadataCSVMixin(object):

    def metadata(self, fp, timeout=10):
        """
        Download the metadata CSV for this group
        """
        url = 'analytics/groups/{}/metadata'.format(self.id)
        return self._client.request_to_file(fp, 'GET', url, timeout=timeout)
