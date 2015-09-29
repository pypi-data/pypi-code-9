from paom.base import BaseResource


class Users(BaseResource):

    ABSOLUTE_URL = "/users/"

    def favorites(self, username):
        url = "%s%s" % ("/user-favorites/", username)
        return  self.request._call_api(url)

    def follow(self, data):
        """
        Allows a user to follow another user. 'data' param should
        contain:
            'follower': serialized user who is the follower
            'followed': serialized user who is being followed
        """
        url = "/user-follows/"
        return  self.request._call_api(url, data=data, method="POST")

    def unfollow(self, data):
        """
        Allows a user to unfollow another user. 'data' param should
        contain:
            'follower': serialized user who is the follower
            'followed': serialized user who is being followed
        """
        url = "/user-unfollow/"
        return  self.request._call_api(url, data=data, method="DELETE")

    def favorite_product(self, data):
        """
        Allows a user to favorite a product. 'data' param should
        contain:
            'paomuser': serialized user
            'product': serialized product
        """
        url = "/user-favorites/"
        return  self.request._call_api(url, data=data, method="POST")

    def unfavorite_product(self, data):
        """
        Allows a user to favorite a product. 'data' param should
        contain:
            'paomuser': serialized user
            'product': serialized product
        """
        url = "/user-unfavorite/"
        return  self.request._call_api(url, data=data, method="DELETE")

