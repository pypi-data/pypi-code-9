from warnings import warn
from sirql.SiRQLCondition import SiRQLCondition

__author__ = 'cansik'


class SiRQLBuilder(object):
    def __init__(self):
        self.__conditions = []

    def __append(self, condition):
        self.__conditions.append(condition)

    @staticmethod
    def as_string(element):
        return '"%s"' % element

    def build(self):
        """
        Creates a string out of all conditions.
        :return: Returns a SiRQL string.
        """
        warn("Use another method!", DeprecationWarning)
        return '&'.join(map(str, self.__conditions))

    def collect(self):
        """
        Returns the conditions.
        :return: Returns the conditions.
        """
        return self.__conditions

    def lt(self, field, value):
        con = SiRQLCondition(field, 'lt', value)
        self.__append(con)
        return self

    def gt(self, field, value):
        con = SiRQLCondition(field, 'gt', value)
        self.__append(con)
        return self

    def between(self, field, lower, upper):
        con = SiRQLCondition(field, 'between', lower, upper)
        self.__append(con)
        return self

    def eq(self, field, *values):
        con = SiRQLCondition(field, 'eq', *values)
        self.__append(con)
        return self

    def like(self, field, value):
        con = SiRQLCondition(field, 'like', value)
        self.__append(con)
        return self

    # use ist because is is a keyword
    def ist(self, field, value):
        con = SiRQLCondition(field, 'is', value)
        self.__append(con)
        return self

    def contains(self, field, value):
        con = SiRQLCondition(field, 'contains', value)
        self.__append(con)
        return self
