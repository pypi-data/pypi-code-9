#!/usr/bin/python

"""
This module contains a few simple core rudiments related to PowerDNS
"""


class PDNSInvalidQueryException(Exception):
    """ Raise this when query can't be parsed. """
    pass


class PDNSHandShakeException(Exception):
    """ Raise this when handshake fails """
    pass


class PDNSUnsupportedQueryException(Exception):
    """ Raise this when your backend doesnt't implement a query type. """
    pass


class PDNSRecord(object):

    """ Basic PowerDNS record """

    def __init__(self, qname, qclass, qtype, ttl, qid, content):
        self.__qname = qname
        self.__qclass = qclass
        self.__qtype = qtype
        self.__ttl = ttl
        self.__id = qid if qid else -1
        self.__content = content

    def to_response_line(self):
        """ Get the response line for this record. """
        return "\t".join([self.__qname, self.__qclass,
                          self.__qtype, "%d" % self.__ttl, "%d" % self.__id,
                          self.__content])


class PDNSQuery(object):

    """ This is what a query from PowerDNS through pipe backend looks like """

    def __init__(self, cmd, qname, qtype, qclass, qid, remote_ip, local_ip=None,
                 edns_subnet=None):
        self.__cmd = cmd
        self.__qname = qname
        self.__qtype = qtype
        self.__qclass = qclass
        self.__qid = int(qid)
        self.__remote_ip = remote_ip
        self.__local_ip = local_ip
        self.__edns_subnet = edns_subnet

    def get_cmd(self):
        return self.__cmd

    def get_qname(self):
        return self.__qname

    def get_qtype(self):
        return self.__qtype

    def get_qclass(self):
        return self.__qclass

    def get_qid(self):
        return self.__qid

    def get_remote_ip(self):
        return self.__remote_ip

    def get_local_ip(self):
        return self.__local_ip

    def get_ends_subnet(self):
        return self.__edns_subnet


