
""" Core concepts for PowerDNS backends """

import re


Q_SEPARATOR = "\t"
HELO_REGEX = re.compile("^(HELO)%s([1-3]{1})$" % Q_SEPARATOR)


class PDNSHandshakeException(Exception):
    pass


class QueryParseException(Exception):
    pass


class PDNSRecord(object):

    def __init__(self, name: str, result_class: str, type: str, ttl: int,
                 q_id: int, content: str):
        self.__name = name
        self.__result_class = result_class
        self.__type = type
        self.__ttl = ttl
        self.__q_id = q_id
        self.__content = content

    def get_name(self):
        return self.__name

    def get_class(self):
        return self.__result_class

    def get_type(self):
        return self.__type

    def get_ttl(self) ->int:
        return self.__ttl

    def get_id(self) ->int:
        return self.__q_id

    def get_content(self):
        return self.__content


class PDNSQuery(object):

    def __init__(self, abi_version: int, q_command: str, q_name: str,
                 q_type: str, q_class: str, q_id: str, q_remote_ip: str,
                 local_ip_address=None, ends_subnet_address=None):
        self.__abi_version = abi_version
        self.__q_command = q_command
        self.__q_name = q_name
        self.__q_class = q_class
        self.__q_type = q_type
        self.__q_id = int(q_id)
        self.__q_remote_ip = q_remote_ip
        self.__local_ip_address = local_ip_address
        self.__edns_subnet_address = ends_subnet_address

    def get_abi_version(self):
        return self.__abi_version

    def get_command(self) ->str:
        return self.__q_command

    def get_name(self) ->str:
        return self.__q_name

    def get_class(self) ->str:
        return self.__q_class

    def get_type(self) ->str:
        return self.__q_type

    def get_id(self) ->int:
        return self.__q_id

    def get_remote_ip(self) ->str:
        return self.__q_remote_ip

    def get_local_ip(self) ->str:
        if self.__abi_version < 2:
            raise Exception("Query has no local ip, abi version %d" %
                            self.__abi_version)
        return self.__local_ip_address

    def get_ends_subnet_address(self) ->str:
        if self.__abi_version < 3:
            raise Exception("Query has edns subnet address, abi version %d" %
                            self.__abi_version)
        return self.__edns_subnet_address
