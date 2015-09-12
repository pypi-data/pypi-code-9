import json
import logging
from uuid import uuid4
from bigben.errors import BigBenHttpError, BigBenError

# Hack to make this python2/3 compatible
try:
    import urllib2
    from urllib2 import HTTPError, URLError
    from urllib import urlencode
except ImportError:
    from urllib.error import URLError, HTTPError
    from urllib import request as urllib2
    import urllib.parse as urlencode

"""
    A central location to set headers and create web service clients.
"""


class Client(object):
    """
        A central location to set headers and create web service clients.

        Attributes:
            api_token: A string containing your BigBen API developer token.
            user_agent: An arbitrary string which will be used to identify your
                application
            api_version: The version of the API to use. Defaults to 'v1'.

    """
    def __init__(self, api_token, user_agent, api_version="v1"):
        """
            Initializes a BigBen client.

            Args:
                api_token: A string containing your BigBen API developer token.
                user_agent: An arbitrary string which will be used to identify your
                    application.
                api_version: The version of the API to use. Defaults to 'v1'.
        """

        self.api_token = api_token
        self.user_agent = user_agent
        self.api_version = api_version

    def delete_job(self, job_id):
        """
            Deletes an existing job.

            Args:
                job_id: The id of the job to be delete, as a LongType
        """
        request_url = self.__build_url(Client.__JOBS_RELATIVE_URL) + "/" + str(job_id)
        return self.__execute_request(urllib2.Request(request_url,
                                                      headers=self.__build_headers()),
                                      "DELETE"
                                      )

    def update_job(self, job_id, name, schedule, is_active, http_method, http_url, max_num_tries, http_payload={}, http_headers=[]):
        """
            Updates an existing job..

            Args:
                job_id: The id of the job to be updated, as a LongType
                name: The name of this job, as a StringType
                schedule: The cron schedule of this job, as a StringType
                is_active: Flag indicating whether this job is active, as a BooleanType
                http_method: The HTTP method used by this job, as a StringType
                http_url: The HTTP url used by this job, as a StringType
                max_num_tries: The maximum number of tries before the job is 'failed', as an IntType
                http_payload: Optional dictionary containing the payload to be sent with POST requests, as a DictType
                http_headers: Optional dictionary containing the headers to be sent with the request, as a ListType

            Returns:
                A dictionary representing the newly updated job.

        """
        data = {
            'name': name,
            'environment_id': "1", # Hardcoded to one since it's ignored on updates but makes the API more consistent
            'schedule': schedule,
            'is_active': is_active,
            'http_method': http_method,
            'http_url': http_url,
            'max_num_tries': max_num_tries,
            'http_payload': http_payload,
            'http_headers': http_headers,
        }

        request_url = self.__build_url(Client.__JOBS_RELATIVE_URL) + "/" + str(job_id)
        return self.__execute_request(urllib2.Request(request_url,
                                                      data=json.dumps(data),
                                                      headers=self.__build_headers()),
                                      "PUT"
                                      )

    def create_job(self, environment_id, name, schedule, is_active, http_method, http_url, max_num_tries, http_payload={}, http_headers=[]):
        """
            Creates a new job..

            Args:
                environment_id: The environment id of this job, as a LongType
                name: The name of this job, as a StringType
                schedule: The cron schedule of this job, as a StringType
                is_active: Flag indicating whether this job is active, as a BooleanType
                http_method: The HTTP method used by this job, as a StringType
                http_url: The HTTP url used by this job, as a StringType
                max_num_tries: The maximum number of tries before the job is 'failed', as an IntType
                http_payload: Optional dictionary containing the payload to be sent with POST requests, as a DictType
                http_headers: Optional dictionary containing the header to be sent with the request, as a ListType

            Returns:
                A dictionary representing the newly created job.
        """
        data = {
            'environment_id': environment_id,
            'name': name,
            'schedule': schedule,
            'is_active': is_active,
            'http_method': http_method,
            'http_url': http_url,
            'max_num_tries': max_num_tries,
            'http_payload': http_payload,
            'http_headers': http_headers,
        }

        request_url = self.__build_url(Client.__JOBS_RELATIVE_URL)
        return self.__execute_request(urllib2.Request(request_url,
                                                      data=json.dumps(data),
                                                      headers=self.__build_headers()),
                                      "POST"
                                      )

    def get_job(self, job_id):
        """
            Returns a job.

            Args:
                job_id: The id of the job to return, as a LongType

            Returns:
                Returns a dictionary object for the job matched by job_id
                in the following format:
                {
                    'id': LongType,
                    'environment_id': LongType,
                    'name': StringType,
                    'schedule': StringType,
                    'is_active': BooleanType,
                    'http_method': StringType,
                    'http_url': StringType,
                    'http_payload: DictType,
                    'http_headers: ListType,
                    'max_num_tries': IntType,
                    'created_at': datetime.datetime,
                    'updated_at': datetime.datetime
                }
        """
        request_url = self.__build_url(Client.__JOBS_RELATIVE_URL) + "/" + str(job_id)
        return self.__execute_request(urllib2.Request(request_url,
                                                      headers=self.__build_headers()),
                                      "GET"
                                      )

    def list_jobs(self, environment_id=None, name=None):
        """
            Returns a list a jobs.

            Args:
                environment_id: An optional ID of the environment to filter on, as a StringType
                name: An optional string of the job name to filter on, as a StringType

            Returns:
                Yields a dictionary object for each job matching the provided criteria
                in the following format:
                {
                    'id': LongType,
                    'environment_id': LongType,
                    'name': StringType,
                    'schedule': StringType,
                    'is_active': BooleanType,
                    'http_method': StringType,
                    'http_url': StringType,
                    'http_payload: DictType,
                    'http_headers: ListType,
                    'max_num_tries': IntType,
                    'created_at': datetime.datetime,
                    'updated_at': datetime.datetime
                }
        """
        data = {}

        if environment_id is not None:
            data['environment_id'] = environment_id
        if name is not None:
            data['name'] = name

        request_url = self.__build_url(Client.__JOBS_RELATIVE_URL, urlencode(data))
        return self.__execute_request(urllib2.Request(request_url,
                                                      headers=self.__build_headers()),
                                      "GET"
                                      )

    def __execute_request(self, url_request, http_method="GET"):
        """
            Executes the provided URL Request.

            Args:
                url_request: A urllib2.Request object to be executed

            Returns:
                The payload if the call is successful.
        """
        execution_id = uuid4()
        self.__log_request(execution_id, url_request, http_method)
        try:
            # Hack so I don't have to use the requests library.  I probably
            # should in the future though.
            url_request.get_method = lambda: http_method
            url_request.add_header('Content-Type', 'application/json')

            response = urllib2.urlopen(url_request)
            if response.code != 204: # No content to decode, so don't return anything
                return json.loads(response.read())
        except HTTPError as http_error:
            # Get the internal error code and message
            response_dict = json.loads(http_error.read())
            errors = response_dict['errors']

            # Only one is ever returned
            error = errors[0]
            raise BigBenHttpError(http_error.code, error['code'], error['message'])
        except URLError as url_error:
            # Url errors have no info
            raise BigBenError(url_error.reason)
        except Exception as exc:
            # TODO: Handle these.  What if it can't parse the JSON?
            raise

    def __build_url(self, relative_url, querystring_params=None):
        """
            Builds a URL containing the necessary information needed to interact with the
            API.

            Args:
                relative_url: A string representing the relative url
                querystring_params: A optional urlencoded string representing any additional querystring
                    params required to be sent along in the request.

            Returns:
                A string representing the full URL of the resource.
        """
        url = Client.__BASE_URL + self.api_version + relative_url
        if querystring_params:
            url += '?' + querystring_params
        return url

    def __build_headers(self):
        """
            Builds a dictionary containing the necessary headers needed to interact with the
            API.

            Returns:
                A dictionary in the following format:
                {
                    'X-API-Token': StringType,
                    'X-User-Agent': StringType,
                    'X-API-Version': StringType,
                }
        """

        return {
            'X-API-Token': self.api_token,
            'X-User-Agent': self.user_agent,
            'X-API-Version': self.api_version,
        }

    def __log_request(self, execution_id, url_request, http_method):
        """
            Logs the request for debugging purposes.

            Args:
                url_request: The url request object being executed
                http_method: The http method being used, as a StringType
        """
        header_list = ["%s: %s" % (key, value) for key, value in url_request.headers.items()]
        payload = url_request.data
        Client.__LOGGER.debug("Start of execution of %s request: %s. HEADERS: %s. PAYLOAD: %s",
                              http_method,
                              url_request.get_full_url(),
                              header_list,
                              payload)


    # Base service url
    __BASE_URL = "http://cuebigben.io/api/"

    # Jobs relative url
    __JOBS_RELATIVE_URL = '/jobs'

    # Logger for all bigben related transport
    __LOGGER = logging.getLogger("bigben.transport")

    __slots__ = (
        'api_token',
        'user_agent',
        'api_version',
    )
