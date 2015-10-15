from generic_client import PredataGenericClient


class PredataSignalClient(PredataGenericClient):

    """
    Client for requesting Predata signals.
    """

    def _handle_special_endpoints(self, endpoint, maximum, normalized):
        if maximum:
            endpoint += "max/"
        elif normalized:
            endpoint += "norm/"
        return endpoint

    def get_source_signal(self, source_id, signal_type="signals", date=None, maximum=False, normalized=False):
        """
        Get source signal by source id.

        Accepts difference signal type ("signals", "chatter", "contestation", "users")
        """
        endpoint = "data/source/%s/" % signal_type
        endpoint = self._handle_special_endpoints(endpoint, maximum, normalized) + "?source_id=%s" % (source_id)
        if date:
            endpoint += "&date=%s" % date.isoformat()
        return {
            "source": source_id,
            "signal_type": signal_type,
            "max": maximum,
            "normalized": normalized,
            "date": date,
            "result": self.make_request(endpoint)
        }

    def list_source_signal(self, source_id):
        """
        TODO: Return all signals associated with source

        i.e. for a given source, what set of chatter, contestation, user, signal is available
        in future, moving averages, transformations, etc.
        """
        raise NotImplementedError()

    def get_country_signal(self, code, date=None, maximum=False, normalized=False):
        """
        Get country signal by country code.
        """
        endpoint = "data/country/signals/"
        endpoint = self._handle_special_endpoints(endpoint, maximum, normalized) + "?iso3=%s" % code
        if date:
            endpoint += "&date=%s" % date.isoformat()
        return {
            "country": code,
            "max": maximum,
            "normalized": normalized,
            "date": date,
            "result": self.make_request(endpoint)
        }

    def list_country_signal(self, iso3):
        """
        TODO: Return all signals associated with country
        """
        raise NotImplementedError()

    def get_topic_signal(self, topic_id, date=None, maximum=False, normalized=False):
        """
        Get topic signal by topic_id.
        """
        endpoint = "data/topic/signals/"
        endpoint = self._handle_special_endpoints(endpoint, maximum, normalized) + "?topic_id=%s" % topic_id
        if date:
            endpoint += "&date=%s" % date.isoformat()
        return {
            "topic": topic_id,
            "max": maximum,
            "normalized": normalized,
            "date": date,
            "result": self.make_request(endpoint)
        }

    def list_topic_signals(self, topic_id):
        """
        TODO: Return all signals associated with topic
        """
        raise NotImplementedError()
