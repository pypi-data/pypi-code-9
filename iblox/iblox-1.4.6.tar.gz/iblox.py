# coding=utf-8
"""A python module for interacting with the Infoblox WAPI.  The module supports auth sessions via the
requests module as well as numerous shortcuts for manipulating objects within Infoblox."""
# Copyright (C) 2015 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json


class MissingRequiredArgument(Exception):
    """A required argument was missing from your statement
    """
    pass


class HostNotFound(Exception):
    """Unable to find host in Infoblox
    """
    pass


class UnknownReturnType(Exception):
    """You specified a return time that is not supported
    """
    pass


def ipv4addr_obj(ipaddr, **kwargs):
    """Create a new IPv4 Address dictionary

    - **parameters** and **return types**::

        :param ipaddr: ipv4 address
        :param kwargs: key/value options for ipv4addr object
        :return: ipvraddr dictionary with default values
    """
    ipv4_obj = {'configure_for_dhcp': False, 'ipv4addr': ipaddr}
    for key, value in kwargs.iteritems():
        ipv4_obj[key] = value
    return ipv4_obj


class Infoblox(object):
    """Create a new instance of the Infoblox WAPI Object

        - **parameters** and **return types**::

            :param uri: Full url to the Infoblox WAPI
            :param username: Infoblox User with API Access
            :param password: Password for Infoblox User
            :param verify_ssl: Verify SSL Certificate
            :return: Infoblox Object

        - **properties**:

            :property view: The DNS view to add objects to (default is 'default')
        """
    def __init__(self, uri, username=None, password=None, verify_ssl=False):
        if uri.endswith("/") is False:
            uri += "/"
        self.uri = uri
        self.auth = (username, password)
        self.verify = verify_ssl
        self._return_type = "json"  # This is what the WAPI defaults to
        self.returnTypes = ('json', 'json-pretty', 'xml', 'xml-pretty')
        self.session = requests.Session()
        self.view = 'default'
        if verify_ssl is False:
            # This is so you don't get weird warning messages about not verifying ssl certs
            try:
                requests.packages.urllib3.disable_warnings()
            except AttributeError:
                pass

    def __str__(self):
        return str(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def _verify_(self, **kwargs):
        """Private method for verifying the named argument data and preparing it for a wapi call

        .. note::
            Key modifiers will also be fixed if the key ends in one of the following strings:
                * _plus = +
                * _regex = ~
                * _notequal = !
                * _ignorecase = :
                * _lessthan = <
                * _greaterthan = >

        - **parameters** and **return types**::

            :param kwargs: key/value pairs
            :return: Dictionary ready for wapi call
        """
        nkeys = kwargs.keys()
        if '_ref' not in nkeys and 'objtype' not in nkeys:
            if '_function' not in nkeys:
                raise MissingRequiredArgument("objtype or _ref is required!")

        if "_return_type" in nkeys:
            if kwargs['_return_type'] not in self.returnTypes:
                raise UnknownReturnType(kwargs['_return_type'] + " is not a valid return type!")
            else:
                self._return_type = kwargs['_return_type']

        newdict = {}
        for key, value in kwargs.items():
            if key.endswith("_regex"):
                key = key.replace("_regex", "~")
            elif key.endswith("_plus"):
                key = key.replace("_plus", "+")
            elif key.endswith("_notequal"):
                key = key.replace("_notequal", "!")
            elif key.endswith("_ignorecase"):
                key = key.replace("_ignorecase", ":")
            elif key.endswith("_lessthan"):
                key = key.replace("_lessthan", "<")
            elif key.endswith("_greaterthan"):
                key = key.replace("_greaterthan", ">")
            newdict[key] = value
        return newdict

    def keys(self):
        """Return the object as a dictionary

        - **parameters** and **return types**::

            :return: Dictionary
        """
        return self.__dict__.keys()

    def get(self, **kwargs):
        """ Query the Infoblox WAPI

        Query the Infoblox WAPI for records of a specific type (with or without regular expressions)
        OR
        Query the Infoblox WAPI for a specific record by its _ref

        - **parameters** and **return types**::

            :param kwargs: Key/Value parameters
            :return: string of _return_type (json or xml)
        """
        kwargs = self._verify_(**kwargs)
        nkeys = kwargs.keys()
        if "_ref" in nkeys:
            result = self.session.get(self.uri + kwargs['_ref'], auth=self.auth, verify=self.verify)
        else:
            objtype = kwargs['objtype']
            del kwargs['objtype']
            result = self.session.get(self.uri + objtype, auth=self.auth, verify=self.verify, data=kwargs)
        if self._return_type == 'json':
            return result.json()
        else:
            return result.text

    def add(self, **kwargs):
        """Add a record of a given type to Infoblox via the WAPI

        - **parameters** and **return types**::

            :param kwargs: key/value parameters
            :return: string of _return_type (json or xml)
        """
        kwargs = self._verify_(**kwargs)
        objtype = kwargs['objtype']
        del kwargs['objtype']
        result = self.session.post(self.uri + objtype, auth=self.auth, verify=self.verify, data=json.dumps(kwargs))
        if self._return_type == 'json':
            return result.json()
        else:
            return result.text

    def delete(self, ref, **kwargs):
        """Delete a record in Infoblox based on its _ref id.

        - **parameters** and **return types**::

            :param ref: Reference id for a given object
            :param kwargs: key/value parameters
            :return: string of _return_type (json or xml)
        """
        kwargs['_ref'] = ref
        kwargs = self._verify_(**kwargs)
        del kwargs['_ref']
        result = self.session.delete(self.uri + ref, auth=self.auth, verify=self.verify, data=json.dumps(kwargs))
        if self._return_type == 'json':
            return result.json()
        else:
            return result.text

    def modify(self, ref, **kwargs):
        """Modify/Update an existing object

        - **parameters** and **return types**::

            :param ref: The _ref id of the object to update
            :param kwargs: key/value parameters
            :return: string of _return_type (json or xml)
        """
        kwargs['_ref'] = ref
        kwargs = self._verify_(**kwargs)
        del kwargs['_ref']
        result = self.session.put(self.uri + ref, auth=self.auth, verify=self.verify, data=json.dumps(kwargs))
        if self._return_type == 'json':
            return result.json()
        else:
            return result.text

    def call(self, ref, func, **kwargs):
        """Call a specific function on a given object

        - **parameters** and **return types**::

            :param ref: The _ref of the object
            :param func: The function to call
            :param kwargs: Data to be passed to the function
            :return: String of _return_type(json or xml)
        """
        _function = {'_function': func}
        kwargs['_ref'] = ref
        kwargs = self._verify_(**kwargs)
        del kwargs['_ref']
        result = self.session.post(self.uri + ref, auth=self.auth, verify=self.verify,
                                   params=_function, data=json.dumps(kwargs))
        if self._return_type == 'json':
            return result.json()
        else:
            return result.text

    def get_host(self, **kwargs):
        """Shortcut for finding host records

        - **parameters** and **return types**::

            :param kwargs: Can contain dictionary of data to search for or _ref of specific record
            :return: string of _return_type (json or xml)
        """
        if "_ref" in kwargs.keys():
            return self.get(**kwargs)
        else:
            kwargs['objtype'] = "record:host"
            return self.get(**kwargs)

    def get_host_by_ip(self, ipaddr):
        """Shortcut for finding a host record by its primary IPV4 address

        - **parameters** and **return types**::

            :param ipaddr: IPV4 address
            :return: string of _return_type (json or xml)
        """
        return self.get_host(ipv4addr=ipaddr)

    def get_host_by_name(self, fqdn):
        """Shortcut for finding a host record by its fully qualified domain name

        - **parameters** and **return types**::

            :param fqdn: Fully Qualified Domain Name
            :return: string of _return_type (json or xml)
        """
        return self.get_host(name=fqdn)

    def add_host(self, fqdn, ipaddr, **kwargs):
        """Shortcut for adding a host record with an iPV4 address

        - **parameters** and **return types**::

            :param fqdn: Fully Qualified Domain Name of the host to add
            :param ipaddr: IPV4 address of the host (can be a list of ipv4 addresses)
            :param kwargs: Key/Value dictionary of any extra options to add to host record
            :return: string of _return_type (json or xml)
        """
        ipv4addrs = []
        if type(ipaddr) in (list, tuple):
            for ip in ipaddr:
                ipv4addrs.append(ipv4addr_obj(ip))
        else:
            ipv4addrs.append(ipv4addr_obj(ipaddr))
        newhost = {'objtype': 'record:host', 'name': fqdn, 'ipv4addrs': ipv4addrs, 'view': self.view}
        for key, value in kwargs.iteritems():
            newhost[key] = value
        return self.add(**newhost)

    def add_host_ip(self, fqdn, ipaddr):
        """Shortcut for adding an ip to a given host

        - **parameters** and **return types**::

            :param fqdn: Fully Qualified Domain name of the host
            :param ipaddr: IPV4 address of the host (can be a list of ipv4 addresses)
            :return: Modified host record
        """
        try:
            host = self.get_host_by_name(fqdn)[0]
        except IndexError:
            raise HostNotFound("Unable to find host with name " + fqdn)
        if type(ipaddr) in (list, tuple):
            for ip in ipaddr:
                host['ipv4addrs'].append(ipv4addr_obj(ip))
        else:
            host['ipv4addrs'].append(ipv4addr_obj(ipaddr))
        return self.modify(host['_ref'], ipv4addrs=host['ipv4addrs'])

    def add_alias(self, fqdn, alias):
        """Shortcut for adding an alias/CNAME to a given host record

        - **parameters** and **return types**::

            :param fqdn: Fully Qualified Domain Name of the host
            :param alias: A fqdn name (or list of fqdns) to add as aliases/CNAMES
            :return: string of _return_type (json or xml)
        """
        thishost = self.get_host(name=fqdn, _return_fields_plus="aliases")[0]
        if 'aliases' not in thishost.keys():
            thishost['aliases'] = []
        if type(alias) in (list, tuple):
            for name in alias:
                if name not in thishost['aliases']:
                    thishost['aliases'].append(name)
        else:
            if alias not in thishost['aliases']:
                thishost['aliases'].append(alias)
        return self.modify(thishost['_ref'], aliases=thishost['aliases'])

    def delete_alias(self, fqdn, alias):
        """Shortcut for adding an alias/CNAME to a given host record

        - **parameters** and **return types**::

            :param fqdn: Fully Qualified Domain Name of the host
            :param alias: The fqdn of the alias (or list of fqdns) you wish to remove
            :return: string of _return_type (json or xml)
        """
        thishost = self.get_host(name=fqdn, _return_fields_plus='aliases')[0]
        if 'aliases' not in thishost.keys():
            return thishost
        else:
            if type(alias) in (list, tuple):
                for name in alias:
                    if name in thishost['aliases']:
                        thishost['aliases'].remove(name)
            else:
                thishost['aliases'].remove(alias)
            return self.modify(thishost['_ref'], aliases=thishost['aliases'])
