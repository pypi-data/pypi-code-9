""" a wrapper class for the statuspage.io api"""
import logging
import requests

PRIVATE_API_URL = 'https://api.statuspage.io/v2/pages/'


class StatusPageApiError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class StatusPageComponent(object):
    OPERATIONAL = 'operational'
    DEGRADED_PERFORMANCE = 'degraded_performance'
    PARTIAL_OUTAGE = 'partial_outage'
    MAJOR_OUTAGE = 'major_outage'

    STATUS_LIST = [OPERATIONAL, DEGRADED_PERFORMANCE, PARTIAL_OUTAGE, MAJOR_OUTAGE]

    def __init__(self, id, status, name=None, created_at=None, description=None, page_id=None, position=None, updated_at=None, group_id=None, group=None, only_show_if_degraded=None):
        self.id = id
        self.status = status
        self.created_at = created_at
        self.description = description
        self.name = name
        self.page_id = page_id
        self.position = position
        self.updated_at = updated_at

    # def update(self, new_status, token=None):
    #     if new_status not in StatusPageApi.STATUS_LIST:
    #         raise StatusPageApiError("Not a valid status")
    #     if token is None:
    #         logging.error('Cannot access private APIs without OAuth token')
    #         raise StatusPageApiError("Cannot access private API")
    #     else:


class StatusPageApi(object):

    def __init__(self, organization_id, token=None):
        if organization_id is None:
            raise StatusPageApiError('You must supply organization_id for instructions see https://doers.statuspage.io/api/authentication/')
        self._organization = organization_id
        if token is None:
            logging.warning("without OAuth token you can only access the public api (read only mode)")
        else:
            self._oauth_token = token
        self._public_url = 'https://%s.statuspage.io/api/v2/' % (organization_id)

    def check_status_code(self, response):
        if response.status_code == requests.codes.ok:
            if response.status_code == 200:
                logging.info('request returned ok')
                return "OK"
            if response.status_code == 201:
                logging.info('resource created')
                return "created"
        else:
            json_error = response.json()
            raise StatusPageApi(json_error['errors'])

    def get_all_components(self):
        components = []
        res = requests.get(self._public_url + "components.json")
        self.check_status_code(res)
        for component in res.json()['components']:
            components.append(StatusPageComponent(**component))
        return components

    def update_component(self, component, new_status):
        if new_status not in component.STATUS_LIST:
            raise StatusPageApiError("Not a valid status")
        if self._oauth_token is None:
            logging.error('Cannot access private APIs without OAuth token')
            raise StatusPageApiError("Cannot access private API")
        else:
            header = {'Authorization': 'OAuth ' + self._oauth_token}
            status_change = {"component[status]": new_status}
            url = "%s%s/components/%s.json" % (PRIVATE_API_URL, self._organization, component.id)
            msg = "Changing component %s from %s to %s" % (component.name, component.status, new_status)
            logging.info(msg)
            res = requests.patch(url, data=status_change, headers=header)
            status = self.check_status_code(res)
            logging.info(status)
