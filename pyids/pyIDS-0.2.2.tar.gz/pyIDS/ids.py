import requests
import xmltodict
from workitem import Workitem

# Suppress the warnings for now
requests.packages.urllib3.disable_warnings()


class IDS(object):
    '''
    A class to encapsulate the work needed to send REST calls to the IBM Devops Service RTC backend.
    '''
    def __init__(self, url, user, password):
        self.base_url = url
        self.session = self.create_session(user, password)

    def create_session(self, jazz_user, jazz_password):
        session = requests.Session()
        session.verify = False
        session.allow_redirects = True
        session.headers = {'accept': 'application/json'}
        session.auth = (jazz_user, jazz_password)

        # Request for authenticated resource
        auth_uri = "/authenticated/identity"
        response = session.get(self.base_url + auth_uri, verify=False)

        if response.status_code == 200:
            return session
        elif response.status_code == 401:
            raise Exception("Failed to login! Make sure your username and password are correct.")
        else:
            raise Exception("Unknown error during session create. Response code: %s" % response.status_code)

    def get(self, url):
        return self.session.get(self.base_url + url, verify=False)

    def get_work_items(self, **filters):
        '''
        Get a work item's information
        :param filters: A series of key value pairs to filter on
        :return: list of Workitems or None
        '''
        filter_string = ""
        for key, val in filters.iteritems():
            filter_string += "%s='%s'" % (key, val)
        url = "/rpt/repository/workitem?fields=workitem/workItem[%s]/(" \
              "*|\
               owner/name|\
               state/name|\
               projectArea/name|\
               type/name|\
               comments/*|\
               comments/creator/*|\
               stringComplexity/*|\
               category/*|\
               creator/*|\
               tags/*|\
               priority/*|\
               severity/*\
               )" % filter_string
        try:
            response = self.get(url)
        except requests.exceptions.ReadTimeout:
            return "Request timed out :("

        if response.status_code != 200:
            return None

        output = xmltodict.parse(response.text)
        if "workItem" not in output["workitem"]:
            return None
        else:
            workitems = []
            if isinstance(output["workitem"]["workItem"], list):
                for wi in output["workitem"]["workItem"]:
                    workitems.append(Workitem(wi))
            else:
                workitems.append(Workitem(output["workitem"]["workItem"]))
            return workitems

    def get_work_item_by_id(self, wi_id):
        '''
        Retrieves a single work item based off of the supplied ID

        :param wi_id: The work item ID number
        :return: Workitem or None
        '''
        work_items = self.get_work_items(id=wi_id)
        if work_items is not None:
            return work_items[0]
        return None

    def get_work_items_by_owner(self, wi_owner):
        '''
        Retrieves a list of work items owned by the supplied name

        :param wi_owner: The name of the owner to filter for
        :return: List of Workitems or None
        '''
        owner_filter = {"owner/name": wi_owner}
        return self.get_work_items(**owner_filter)