import urllib

from generic_client import PredataGenericClient


class PredataDataClient(PredataGenericClient):

    """
    Client for requesting Predata data information.
    """

    def list_source(self, country_code=None, topic_id=None):
        """
        List all signals within a domain.
        """
        endpoint = "data/sources/"
        query_dict = {
            "iso3": country_code,
            "topic_id": topic_id
        }
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]})
        endpoint += "?%s" % params
        return {
            "country_code": country_code,
            "topic_id": topic_id,
            "result": self.make_request(endpoint)
        }

    def get_source(self, source_id):
        """
        Get source information.
        """
        endpoint = "data/sources/?source_id=%s" % source_id
        return {
            "source_id": source_id,
            "result": self.make_request(endpoint)
        }

    def list_country(self):
        """
        List all countries.
        """
        endpoint = "data/countries/"
        return {
            "result": self.make_request(endpoint)
        }

    def get_country(self, code):
        """
        Get country data.
        """
        endpoint = "data/countries/%s/" % code
        return {
            "country": code,
            "result": self.make_request(endpoint)
        }

    def list_topic(self):
        """
        List all topics
        """
        endpoint = "data/topics/"
        return {
            "result": self.make_request(endpoint)
        }

    def get_topic(self, topic_id):
        """
        Get topic data.
        """
        endpoint = "data/topics/%s/" % topic_id
        return {
            "topic_id": topic_id,
            "result": self.make_request(endpoint)
        }

    def list_event(self, country_code=None, topic_id=None, tag_id="all"):
        """
        List all events in country by tag.
        """
        endpoint = "data/events/"
        query_dict = {
            "iso3": country_code,
            "topic_id": topic_id,
            "tag_id": tag_id
        }
        params = urllib.urlencode({k: query_dict[k] for k in query_dict.keys() if query_dict[k]})
        endpoint += "?%s" % params
        return {
            "country_code": country_code,
            "topic_id": topic_id,
            "tag_id": tag_id,
            "result": self.make_request(endpoint)
        }

    def get_event(self, event_pk):
        """
        Get event data.
        """
        endpoint = "data/events/%s/" % event_pk
        return {
            "event": event_pk,
            "result": self.make_request(endpoint)
        }

    def list_tags(self, tag_category=None):
        """
        List all tags.

        Filter by tag_category.
        """
        endpoint = "data/tags/"
        if tag_category:
            endpoint += "?tag_category_id=%s" % tag_category
        return {
            "tag_category": tag_category,
            "result": self.make_request(endpoint)
        }

    def get_tag(self, tag_id):
        """
        Get tag data.
        """
        endpoint = "data/tags/%s/" % tag_id
        return {
            "tag_id": tag_id,
            "result": self.make_request(endpoint)
        }

    def list_tag_categories(self, tag_category_id=None):
        """
        Get tag category data.
        """
        endpoint = "data/tagcategories/"
        return {
            "tag_category_id": tag_category_id,
            "result": self.make_request(endpoint)
        }

    def get_tag_category(self, tag_category_id):
        """
        Get tag category.
        """
        endpoint = "data/tagcategories/%s/" % tag_category_id
        return {
            "tag_category_id": tag_category_id,
            "result": self.make_request(endpoint)
        }
