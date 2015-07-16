import requests
import xmltodict
from workitem import Workitem

class IDS(object):
    '''
    A class to encapsulate the work needed to send REST calls to the IBM Devops Service RTC backend.
    '''
    def __init__(self, url, user, password):
        # Creating a RTCClient
        self.base_url = url
        self.session = self.create_session(user, password)
        print "IDS created"

    def create_session(self, jazz_user, jazz_password):
        session = requests.Session()
        session.verify = False
        session.allow_redirects = True
        session.headers = {'accept': 'application/json'}
        session.auth = (jazz_user, jazz_password)

        # Request for authenticated resource
        auth_uri = "/authenticated/identity"
        print self.base_url + auth_uri
        response = session.get(self.base_url + auth_uri, verify=False)

        if 'x-com-ibm-team-repository-web-auth-msg' in response.headers and response.headers['x-com-ibm-team-repository-web-auth-msg'] == 'authrequired':
            login_response = session.post(self.base_url + '/j_security_check',
                                               data={'j_username': jazz_user, 'j_password': jazz_password})

            if 'x-com-ibm-team-repository-web-auth-msg' in login_response.headers and login_response.headers['x-com-ibm-team-repository-web-auth-msg'] == 'authrequired':
                # Failed to authenticate
                raise Exception("Failed to login: ", login_response.text)

            # Getting authenticated resource again now that we should be logged in
            response = session.get(self.base_url + auth_uri)
        else:
            print "Already authenticated."
        return session

    def get(self, url):
        return self.session.get(self.base_url + url, verify=False)

    def get_work_item(self, itemNumber):
        '''
        Get a work item's information
        :param itemNumber: The work item ID number
        :return: Workitem or None
        '''
        url = "/rpt/repository/workitem?fields=workitem/workItem[id=%s]/(" \
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
               )" % itemNumber
        try:
            response = self.get(url)
        except requests.exceptions.ReadTimeout:
            return "Request timed out :("
        output = xmltodict.parse(response.text)
        if "workItem" not in output["workitem"]:
            return None
        else:
            workitem = Workitem(output)
        return workitem