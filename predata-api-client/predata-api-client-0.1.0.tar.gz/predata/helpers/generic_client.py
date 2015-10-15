class PredataGenericClient():

    def __init__(self, session, hostname, api_base):
        self.session = session
        self.HOSTNAME = hostname
        self.API_BASE = api_base

    def make_request(self, endpoint):
        """
        Make and paginate through results if necessary.
        """
        total_response = []
        current_endpoint = self.HOSTNAME + self.API_BASE + endpoint
        while current_endpoint:
            resp = self.session.get(current_endpoint)
            response_content = resp.json()
            if "results" in response_content and response_content["results"] != "processing":
                total_response += response_content["results"]
                if "next" in response_content:
                    current_endpoint = response_content["next"]
                else:
                    current_endpoint = None
            else:
                total_response = response_content
                current_endpoint = None
        return total_response
