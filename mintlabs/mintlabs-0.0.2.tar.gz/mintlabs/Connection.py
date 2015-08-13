import requests
import logging
import json


class Connection:

    """
    The Connection class implements an HTTP connection with the server.
    Once it is instantiated created it will act as an identifier used by
    the rest of objects.

    :param username: username of the platform. To get one go to
                     https://platform.mint-labs.com

    :param password: the password assigned to the username.

    :param test: True -> connection will be done to the testing
                 platform (http://test.mint-labs.com).
                 False -> connection will be done to the platform
                 (http://platform.mint-labs.com).

    :type username: String
    :type password: String
    :type test: Bool

    """

    def __init__(self, username, password, test=False):
        self.cookie = None
        self.username = username
        self.password = password
        if test:
            self.verify_certificates = False
            self.baseurl = "https://test.mint-labs.com"
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        else:
            self.verify_certificates = True
            self.baseurl = "https://platform.mint-labs.com"
        self.login()

    def login(self):
        """Login to the platform."""
        content = self.send_request("login",
                                {"username": self.username, "password": self.password})
        if content["success"]:
            logging.info("Logged in as {0}".format(self.username))
            return True
        else:
            logging.error("Login is invalid")
            return False

    def logout(self):
        """
        Logout from the platform.

        :return: True if logout was successful, False otherwise.
        :rtype: Bool
        """

        content = self.send_request("logout")
        if content["success"]:
            logging.info("Logged out successfully")
            self.cookie = None
            return True
        else:
            logging.error("Logout was unsuccesful")
            return False

    def send_request(self, path, req_parameters={}, req_headers={},
                      stream=False, return_raw_response=False):
        """
        Send a request to the Mint Labs Platform.

        Interaction with the server is performed as POST requests.

        :param req_url:  URL to perform the request. The host should be either
                         "https://test.mint-labs.com"
                         or "https://platform.mint-labs.com".

        :param req_parameters: data to send in the POST request.

        :param req_headers: "extra" headers to include in the request:
                            {"header-name": "value"}.
        :param stream: defer downloading the response body until accessing the
                       Response.content attribute.

        :param return_raw_response: When True, return the response from the server
                                    as-is. When False (by default), parse the
                                    answer as json to return a dictionary.

        :type req_url: String
        :type req_parameters: Dict
        :type req_headers: Dict
        :type stream: Bool
        :type return_raw_response: Bool
        """

        req_url = "{0}/{1}".format(self.baseurl, path)
        if self.cookie is not None:
            req_headers["Cookie"] = self.cookie
        req_headers["Mint-Api-Call"] = 1

        try:
            response = requests.post(req_url,
                                     data=req_parameters,
                                     headers=req_headers,
                                     timeout=900.0,
                                     stream=stream,
                                     verify=self.verify_certificates)
        except Exception as e:
            error = "Could not send request. ERROR: {0}".format(e)
            logging.error(error)
            raise Exception(error)

        # Set the login cookie in our object
        if "set-cookie" in response.headers:
            self.cookie = response.headers["set-cookie"]

        if return_raw_response:
            return response

        if response.status_code == 500:
            error = "Server returned status 500."
            logging.error(error)
            raise Exception(error)

        # raise exception if there is no response from server
        elif not response:
            error = "No response from server."
            logging.error(error)
            raise Exception(error)

        try:
            parsed_content = json.loads(response.text)
        except Exception as e:
            error = "Could not parse the response as JSON data: {}".format(response.text)
            logging.error(error)
            raise Exception(error)

        # If any other request is performed before login, raise an error
        if "error" in parsed_content:
            error = parsed_content["error"] or "Unknown error"
            logging.error(error)
            raise Exception(error)
        else:

            return parsed_content
