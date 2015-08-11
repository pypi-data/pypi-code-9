"""This client lib provides API to access an IoT server instance,
which in turn, provides information to sensor devices monitored by server.
"""


from __future__ import absolute_import
import json

from . import __version__


try:
    from . import IoTurllib3 as IoTurllib
except ImportError:
    from . import IoTurllib2 as IoTurllib


def is_compatible_version(sver, lver):
    smajor, sminor = str(sver).split('.')[:2]
    # lmajor, lminor = str(lver).split('.')[:2]
    return smajor == '1' and 0 <= int(sminor) <= 10


class Group:
    """Creates an IoT Group instance connected to one server,
    which can form a cluster of several servers, as configured by the IoT application.

    :param str server: server url, such as 'http://localhost:9001'
    :param str group: a group of devices that belong to one entity,
                      as 'me' to access local devices or 'friend1'
    :param int timeout: request timeout in seconds
    """
    def __init__(self, server, group, timeout=10):
        self.server = server
        self.group = group
        self.server_url = server + '/' + group
        self.timeout = timeout

        sver = IoTurllib.get(self.server_url + '/version.json', self.timeout)
        if not is_compatible_version(sver['major'] + '.' + sver['minor'], __version__):
            raise RuntimeError('Version of the IoT lib does not match with the server.')

    def get_device_list(self, inactive=False):
        """Gets list of devices from server.

        :returns: list of devices
        :rtype: list of dicts
        :raises: HTTPError, socket.timeout
        """
        uri = self.server_url + ".json"
        if not inactive:
            uri += "?active=true"
        return IoTurllib.get(uri, self.timeout)

    def time(self):
        """Returns current server time.

        :returns: current server time
        :rtype: float
        """
        ts = IoTurllib.get(self.server_url + '/servertime.json', self.timeout)
        try:
            return float(ts['time'])
        except:
            return None

    def run_script(self, script_name, phy_name):
        """Runs a script on a server.

        :returns: state of the script.
        """
        data = {'alias': script_name, 'phy': phy_name}
        return IoTurllib.post(self.server + "/terminal/aliases",
                              json.dumps(data), self.timeout)

    def kill_script(self):
        """Kills currently running script on a server.

        :returns: state of the last script
        """
        self.do('$kill')

    def do(self, command, params=''):
        """Sends a command to a server.
        Refer to server help for a list of available commands, obtainable with the $help command.

        :param str command: name of the command to be executed
        :param str params: optional parameters for the command
        """
        data = {
            'command': command,
            'parameters': params
        }
        return IoTurllib.post(self.server + "/terminal/commands",
                              json.dumps(data), self.timeout)


class Device:
    """Represents an IoT Device in a cluster.

    :param server: a server object
    :param str device: name of the device returned by the get_device_list(),
                       such as 'device0' etc.
    :param bool unit: indicates if unit for params is to be fetched.
    :param bool advanced: fetches advanced params of the device if True
    :param bool development: fetches dev params of the device if True
    """

    def __init__(self, server, device, unit=True, advanced=False, development=False):
        self.server = server
        self.device = device.replace(" ", "_")
        self.unit = unit
        self.advanced = advanced
        self.development = development
        self.ts = None

    def time(self):
        return self.ts

    def get(self, parameter='', after=None, options=False, attributes=None):
        """Retrieves one or more parameters of the device.
        If parameter is specified, then only that param info is fetched.
        Otherwise, all the params are fetched.
        A parameter can have a finite range of values, which can be fetched with ``options=True`` flag.

        :param str parameter: name of the parameter
        :param bool after: wait time?
        :param bool options: flag to determine if param options are to be fetched
        :param str attributes: fetches attributes of the passed value
        :returns: list of values
        :rtype: list
        :raises: HTTPError, socket.timeout
        """
        uri = self.server.server_url + "/"
        uri += self.device + "/"
        uri += parameter.replace('.', '/') + ".json"

        qp = []
        if self.unit:
            qp.append('unit=true')
        if after:
            qp.append('after=' + str(after))
        if self.advanced:
            qp.append('advanced=true')
        if self.development:
            qp.append('development=true')
        if options:
            qp.append('options=true')
        if attributes:
            qp.append('attributes=' + str(attributes))

        qs = '?' + '&'.join(qp) or ''
        uri += qs
        return self._parse_status(IoTurllib.get(uri, self.server.timeout))

    def get_value(self, parameter, after=None):
        """Fetches value of the parameter from Device.

        :param str parameter: name of the parameter whose value is to be fetched
        :returns: value of the parameter
        :raises: HTTPError, socket.timeout
        """
        param = parameter.replace('.', '/')
        result = self.get(param, after)
        return result[param.split('/')[-1]]['value']

    def get_records(self, parameter, time_from=None, time_to='last',
                    limit=None, scale=None, average=None):
        """Retrieves values from record storage.

        time_from provides filter value either as a UTC timestamp
        or as 'first' or 'start' strings to indicate that
        retrieval is to be made from first available record.

        time_to provides filter value either as a UTC timestamp
        or one of 'last' or 'end' strings to indicate that
        retrieval is to be made till last n=limit available records.

        Both scale and limit args limit the number of records being returned.
        However, limit returns records each containing ``N`` property.
        scale arg returns records, each containing ``M`` property.
        They are *mutually exclusive*; providing them both raises ``ValueError``
        with appropriate message.
        If none are provided, then server restricts the number of records by 100
        with each record containing ``N`` property by default.

        average arg can be used only with scale;
        providing average without scale raises ValueError.
        average specifies the number of records to be averaged on
        to determine a single scale value.
        average usage is hinted by ``SD`` property present in the response.

        :param str parameter: parameter name or stringified number
        :param int or str time_from: time from which records are to be fetched
        :param int or str time_to: time till which records are to be fetched
        :param int limit: max number of records to return with ``N`` property in each sample
        :param int scale: max number of records to return with ``M`` property in each sample
        :param int average: number of records to average on in case of scale

        :returns: list of JSON objects
        :rtype: list
        :raises: HTTPError, socket.timeout, ValueError
        """
        if limit and scale:
            raise ValueError('Provide either limit or scale arg. They are mutually exclusive.')
        if average and not scale:
            raise ValueError('average arg can only be used with scale arg.')

        uri = self.server.server_url + "/"
        uri += self.device + "/"
        uri += parameter.replace('.', '/') + ".json"

        qp = []
        if limit:
            qp.append('limit=' + str(limit))
        if scale:
            qp.append('scale=' + str(scale))
        if average:
            qp.append('average=' + str(average))
        if time_from:
            qp.append('from=' + str(time_from))
        if time_to:
            qp.append('to=' + str(time_to))
        if self.advanced:
            qp.append('advanced=true')
        if self.development:
            qp.append('development=true')
        if self.unit:
            qp.append('unit=true')
        qs = '?' + '&'.join(qp) or ''
        uri += qs
        return IoTurllib.get(uri, self.server.timeout)

    def set(self, parameter, data, after=None):
        """Set device variables

        :param str parameter: parameter name or stringified number
        :param str data: variable data in json format

        :returns: result of the set values in json format
        :raises: HTTPError, socket.timeout
        """
        uri = self.server.server_url + "/"
        uri += self.device + "/"
        uri += parameter.replace('.', '/')

        struct = data.copy()
        if after:
            struct["$after"] = after
        if self.advanced:
            struct['advanced'] = True
        if self.development:
            struct['development'] = True

        resp = IoTurllib.post(uri, json.dumps(struct), self.server.timeout)
        return self._parse_status(resp)

    def set_value(self, parameter, data, after=None):
        param = parameter.replace('.', '/')
        result = self.get(param)
        token = param.split('/')[-1]
        result[token]['value'] = data
        result = self.set(param, result, after)
        try:
            return result[token]['value']
        except:
            return result['status']

    def _parse_status(self, result):
        try:
            self.ts = float(result['time'])
        except:
            print("Return struct is missing time specifier")

        status = 'OK'
        try:
            status = result['status']
        except:
            print("Return struct is missing status")

        if status.upper() not in ['OK', 'ACK']:
            raise IOError(status)
        return result


class Parameter:
    """Represents a parameter of a device

    :param Device device: a device object
    :param str parameter: parameter name or stringified number
    """

    def __init__(self, device, parameter):
        self.device = device
        self.parameter = parameter.replace('.', '/')
        self.ts = 0
        self.lunit = None
        self.lvalue = None
        self.struct = self.get()
        param = self.parameter.split('/')[-1]  # Only the last parameter is of interest.

        for v in self.struct.keys():
            if param in v:
                self.key = v

    def time(self):
        return self.ts

    def value(self):
        return self.lvalue

    def unit(self):
        return self.lunit

    def get_value(self, after=None):
        value = self.get(after)
        return value[self.key]['value']

    def get_options(self):
        """Retrieves the list of possible values that the Parameter instance can possess.
        If such a range is defined, then it is returned else None is returned.

        :returns: list of option values else None
        """
        resp = self.get(options=True)
        return resp[self.key].get('options', None)

    def get(self, after=None, options=False, attributes=None):
        resp = self.device.get(self.parameter, after=after,
                               options=options, attributes=attributes)
        return self._parse_status(resp)

    def get_records(self, time_from=None, time_to='last',
                    limit=None, scale=None, average=None):
        resp = self.device.get_records(self.parameter,
                                       time_from=time_from, time_to=time_to,
                                       limit=limit, scale=scale, average=average)
        return self._parse_status(resp)

    def set_value(self, new_value, after=None):
        self.struct[self.key]['value'] = new_value
        self.set(self.struct, after)
        return self.value()

    def set(self, data, after=None):
        """Set values of a given parameter(s)

        :param str data: variable data in json format

        :returns: list of values
        :raises: HTTPError, socket.timeout
        """
        resp = self.device.set(self.parameter, data, after)
        return self._parse_status(resp)

    def _parse_status(self, result):
        try:
            self.ts = float(result['time'])
        except:
            print("Return struct is missing time specifier")

        status = 'OK'
        try:
            status = result['status']
        except:
            print("Return struct is missing status")

        if status.upper() not in ['OK', 'ACK']:
            raise IOError(status)

        try:
            self.lvalue = result[self.key]['value']
        except:
            self.lvalue = 'OK'

        try:
            self.lunit = result[self.key]['unit']
        except:
            self.lunit = None

        return result


# Example, accessing the Walnut and reading the system variables
if __name__ == "__main__":
    me = Group('http://localhost:9001', 'devices')
    print('Show available devices and pick up the first:')
    print(me.get_device_list())
    walnut = Device(me, me.get_device_list()[0]['name'])  # assume we have only walnut in the DB

    print('\nBoard was restarted:')
    print(walnut.get('walnut/sys/restarted'))  # show we can get values in this way

    reset = Parameter(walnut, 'walnut/sys/reset', False, 'ack')
    print('\nLast reset state:')
    print(reset.get_value())

    print('\nRestarting the board ...')
    print(reset.set_value('Reset'))

    print('\nNow board was restarted:')
    print(walnut.get('walnut/sys/restarted'))  # show we can get values in this way
