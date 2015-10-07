# -*- coding: utf-8 -*-

import re
import sys
import struct


class ReplayParser:

    SERVER_REGEX = r'((EU|USE|USW|OCE|SAM)\d+(-[A-Z][a-z]+)?)'

    def __init__(self, debug=False):
        self.debug = debug

    def parse(self, replay_file):
        # Work out what type of file we're dealing with.
        if hasattr(replay_file, 'read'):
            replay_file.seek(0)
        elif hasattr(replay_file, 'file'):
            replay_file = open(replay_file.file.path, 'rb')
        else:
            raise Exception("Unable to determine file type.")

        data = {}
        # TODO: CRC, version info, other stuff
        data['crc_check'] = replay_file.read(20)
        data['version'] = replay_file.read(23)
        replay_file.seek(1, 1)

        data['header'] = self._read_properties(replay_file)

        if 'Team0Score' not in data['header']:
            data['header']['Team0Score'] = 0

        if 'Team1Score' not in data['header']:
            data['header']['Team1Score'] = 0

        self.number_of_goals = data['header']['Team0Score'] + data['header']['Team1Score']

        if self.number_of_goals == 0 and 'Goals' not in data['header']:
            data['header']['Goals'] = []

        unknown = self._read_unknown(replay_file, 8)

        data['level_info'] = self._read_level_info(replay_file)

        data['key_frames'] = self._read_key_frames(replay_file)

        data['network_stream'] = self._read_network_stream(replay_file)

        data['debug_strings'] = self._read_debug_strings(replay_file)

        data['goal_ticks'] = self._read_goal_ticks(replay_file)

        data['packages'] = self._read_packages(replay_file)

        data['objects'] = self._read_objects(replay_file)

        data['name_table'] = self._read_name_table(replay_file)

        data['class_index_map'] = self._read_class_index_map(replay_file)

        data['class_net_cache_map'] = self._read_class_net_cache_map(replay_file)

        # Run some manual parsing operations.
        data = self.manual_parse(data, replay_file)

        # data['network_stream'] = self._process_network_stream(data['network_stream'])
        return data

    def _read_properties(self, replay_file):
        results = {}

        while True:
            property_info = self._read_property(replay_file)

            if property_info:
                results[property_info['name']] = property_info['value']
            else:
                return results

    def _read_property(self, replay_file):
        if self.debug:
            print("Reading name")

        name_length = self._read_integer(replay_file, 4)

        property_name = self._read_string(replay_file, name_length)

        if self.debug:
            print("Property name: {}".format(property_name))

        if property_name == 'None':
            return None

        if self.debug:
            print("Reading type")

        type_length = self._read_integer(replay_file, 4)
        type_name = self._read_string(replay_file, type_length)

        if self.debug:
            print("Type name: {}".format(type_name))

        if self.debug:
            print("Reading value")

        if type_name == 'IntProperty':
            value_length = self._read_integer(replay_file, 8)
            value = self._read_integer(replay_file, value_length)

        elif type_name == 'StrProperty':
            unknown = self._read_integer(replay_file, 8)
            length = self._read_integer(replay_file, 4)

            if length < 0:
                length = abs(length) * 2
                value = self._read_string(replay_file, length)[:-1].decode('utf-16').encode('utf-8')
            else:
                value = self._read_string(replay_file, length)

        elif type_name == 'FloatProperty':
            length = self._read_integer(replay_file, 8)
            value = self._read_float(replay_file, length)

        elif type_name == 'NameProperty':
            unknown = self._read_integer(replay_file, 8)
            length = self._read_integer(replay_file, 4)
            value = self._read_string(replay_file, length)

        elif type_name == 'ArrayProperty':
            # I imagine that this is the length of bytes that the data
            # in the "array" actually take up in the file.
            unknown = self._read_integer(replay_file, 8)
            array_length = self._read_integer(replay_file, 4)

            value = [
                self._read_properties(replay_file)
                for x in range(array_length)
            ]

        if self.debug:
            print("Value: {}".format(value))

        return {'name': property_name, 'value': value}

    def _read_level_info(self, replay_file):
        map_names = []
        number_of_maps = self._read_integer(replay_file, 4)

        for x in xrange(number_of_maps):
            map_name_length = self._read_integer(replay_file, 4)
            map_name = self._read_string(replay_file, map_name_length)
            map_names.append(map_name)

        return map_names

    def _read_key_frames(self, replay_file):
        number_of_key_frames = self._read_integer(replay_file, 4)

        key_frames = [
            self._read_key_frame(replay_file)
            for x in range(number_of_key_frames)
        ]

        return key_frames

    def _read_key_frame(self, replay_file):
        time = self._read_float(replay_file, 4)
        frame = self._read_integer(replay_file, 4)
        file_position = self._read_integer(replay_file, 4)

        return {
            'time': time,
            'frame': frame,
            'file_position': file_position
        }

    def _read_network_stream(self, replay_file):
        array_length = self._read_integer(replay_file, 4)

        network_stream = self._read_unknown(replay_file, array_length)

    def _read_debug_strings(self, replay_file):
        array_length = self._read_integer(replay_file, 4)

        if array_length == 0:
            return []

        debug_strings = []

        unknown = self._read_integer(replay_file, 4)

        while len(debug_strings) < array_length:
            name_length = self._read_integer(replay_file, 4)
            player_name = self._read_string(replay_file, name_length)

            debug_string_length = self._read_integer(replay_file, 4)
            debug_string = self._read_string(replay_file, debug_string_length)

            debug_strings.append({
                'PlayerName': player_name,
                'DebugString': debug_string,
            })

            if len(debug_strings) < array_length:
                # Seems to be some nulls and an ACK?
                unknown = self._read_integer(replay_file, 4)

        return debug_strings

    def _read_goal_ticks(self, replay_file):
        goal_ticks = []

        num_goals = self._read_integer(replay_file, 4)

        for x in range(num_goals):
            length = self._read_integer(replay_file, 4)
            team = self._read_string(replay_file, length)
            frame = self._read_integer(replay_file, 4)

            goal_ticks.append({
                'Team': team,
                'frame': frame,
            })

        return goal_ticks

    def _read_packages(self, replay_file):
        num_packages = self._read_integer(replay_file, 4)

        packages = []

        for x in range(num_packages):
            string_length = self._read_integer(replay_file, 4)
            packages.append(self._read_string(replay_file, string_length))

        return packages

    def _read_objects(self, replay_file):
        num_objects = self._read_integer(replay_file, 4)

        objects = []

        for x in range(num_objects):
            string_length = self._read_integer(replay_file, 4)
            objects.append(self._read_string(replay_file, string_length))

        return objects

    def _read_name_table(self, replay_file):
        name_table_length = self._read_integer(replay_file, 4)

        if name_table_length == 0:
            return []
        else:
            # We haven't had this situation yet.
            raise Exception('Name table length was not 0.')
            return []

    # XXX: This is a bit iffy. Check how it works.
    def _read_class_index_map(self, replay_file):
        class_index_map_length = self._read_integer(replay_file, 4)

        class_index_map = {}

        for x in range(class_index_map_length):
            length = self._read_integer(replay_file, 4)
            name = self._read_string(replay_file, length)
            integer = self._read_integer(replay_file, 4)

            class_index_map[integer] = name

        return class_index_map

    def _read_class_net_cache_map(self, replay_file):
        class_net_cache_map = []

        # Read to EOF.
        while True:
            try:
                class_net_cache_map.append(
                    (self._read_integer(replay_file, 4), self._read_integer(replay_file, 4),)
                )
            except Exception as e:
                break

        return class_net_cache_map

    # Temporary method while we learn the replay format.
    def manual_parse(self, results, replay_file):
        server_regexp = re.compile(self.SERVER_REGEX)

        replay_file.seek(0)
        search = server_regexp.search(replay_file.read())
        if search:
            results['header']['ServerName'] = search.group()

        return results

    ##################
    # Helper functions
    ##################

    def _debug_bits(self, replay_file, labels=None):
        byte = replay_file.read(1)
        output = ()

        for index in xrange(8):
            i, j = divmod(index, 8)

            if ord(byte[i]) & (1 << j):
                value = '1'
            else:
                value = '0'

            formatted = value.rjust(index+1, '.').ljust(8, '.')
            output = output + (int(value),)

            if labels and len(labels) == 8:
                print('{} = {}: {}'.format(
                    formatted,
                    labels[index],
                    'Set' if formatted == '1' else 'Not set',
                ))
            else:
                print(value.rjust(index+1, '.').ljust(8, '.'))

        return output

    def _read_bit(self, string, index):
        i, j = divmod(index, 8)

        if ord(string[i]) & (1 << j):
            return 1
        else:
            return 0

    def _pretty_byte_string(self, bytes_read):
        return ' '.join("{:02x}".format(ord(x)) for x in bytes_read)

    def _print_bytes(self, bytes_read):
        print('Hex read: {}'.format(self._pretty_byte_string(bytes_read)))

    def _read_integer(self, replay_file, length, signed=True):
        if signed:
            number_format = {
                1: '<b',
                2: '<h',
                4: '<i',
                8: '<q',
            }[length]
        else:
            number_format = {
                1: '<B',
                2: '<H',
                4: '<I',
                8: '<Q'
            }[length]

        bytes_read = replay_file.read(length)
        if self.debug:
            self._print_bytes(bytes_read)
        value = struct.unpack(number_format, bytes_read)[0]
        if self.debug:
            print("Integer read: {}".format(value))
        return value

    def _read_float(self, replay_file, length):
        number_format = {
            4: '<f',
            8: '<d'
        }[length]

        bytes_read = replay_file.read(length)

        if self.debug:
            self._print_bytes(bytes_read)

        value = struct.unpack(number_format, bytes_read)[0]

        if self.debug:
            print("Float read: {}".format(value))

        return value

    def _read_unknown(self, replay_file, num_bytes):
        bytes_read = replay_file.read(num_bytes)

        if self.debug:
            self._print_bytes(bytes_read)

        return bytes_read

    def _read_string(self, replay_file, length):
        bytes_read = replay_file.read(length)[0:-1]

        if self.debug:
            self._print_bytes(bytes_read)

        return bytes_read

    def _sniff_bytes(self, replay_file, size):
        b = self._read_unknown(replay_file, size)

        print("**** BYTES ****")
        print("Bytes: {}".format(self._pretty_byte_string(b)))
        print('Size:', size)

        if size == 2:
            print("Short: Signed: {} Unsigned: {}".format(struct.unpack('<h', b), struct.unpack('<H', b)))
        else:
            if size == 4:
                print("Integer: Signed: {}, Unsigned: {}".format(struct.unpack('<i', b), struct.unpack('<I', b)))
                print("Float: {}".format(struct.unpack('<f', b)))
            print("String: {}".format(b))


if __name__ == '__main__':
    filename = sys.argv[1]
    if not filename.endswith('.replay'):
        sys.exit('Filename {} does not appear to be a valid replay file'.format(filename))

    with open(filename, 'rb') as replay_file:
        try:
            results = ReplayParser(debug=False).parse(replay_file)
            print(results)
        except IOError as e:
            print(e)
        except struct.error as e:
            print(e)
        except Exception as e:
            print(e)
