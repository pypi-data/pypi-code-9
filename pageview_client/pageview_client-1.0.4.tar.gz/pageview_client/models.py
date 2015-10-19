"""
simple objects for working with returned pageview data
"""


class Trend(object):
    """an object representing a row in the *_trends tables
    """

    def __init__(self, content_id, score):
        """initializes a Trend object

        :param content_id: the primary key of a piece of content
        :type content_id: int

        :param score: the total number of views for the piece of content given a period of time from the request/query
        :type score: int
        """
        self.content_id = content_id
        self.score = score

    def __str__(self):
        """returns a string representation of the object

        :return: a string representation of the object
        :rtype: str
        """
        return "<Trend: content_id={} score={}>".format(self.content_id, self.score)

    def __repr__(self):
        """returns a string representation of the object

        :return: a string representation of the object
        :rtype: str
        """
        return str(self)

    def __lt__(self, other):
        """compares this instance to another based on their `score` attributes

        :param other: the other Trend object to compare
        :type other: Trend

        :return: is self.score less than the other score
        :rtype: bool
        """
        return self.score < other.score
