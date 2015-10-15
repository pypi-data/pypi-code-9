from generic_client import PredataGenericClient


class PredataSystemClient(PredataGenericClient):

    """
    Client for requesting Predata system information.
    """

    def list_user(self, group_id=None):
        """
        Return list of users.
        """
        endpoint = "users/"
        if group_id:
            endpoint += "?group_id=%s" % group_id
        return {
            "group_id": group_id,
            "result": self.make_request(endpoint)
        }

    def get_user(self, user_id):
        """
        Get user information.
        """
        endpoint = "users/%s/" % user_id
        return {
            "user_id": user_id,
            "result": self.make_request(endpoint)
        }

    def list_group(self):
        """
        Return list of groups.
        """
        endpoint = "groups/"
        return {
            "result": self.make_request(endpoint)
        }

    def get_group(self, group_id):
        """
        Get group information.
        """
        endpoint = "groups/%s/" % group_id
        return {
            "group_id": group_id,
            "result": self.make_request(endpoint)
        }
