# -*- coding: utf-8 -*-

import os


def read_last_lines_from_file(file_path, lines, buffer_size=1024):
    """
    Read num of last lines from file.

    :param file_path: path to file
    :param lines: number of lines
    :param buffer_size: buffer size
    """
    file_size = os.stat(file_path).st_size

    i = 0

    with open(file_path) as f:
        if buffer_size > file_size:
            buffer_size = file_size - 1

        data = []

        while len(data) < lines:
            i += 1
            f.seek(file_size - buffer_size * i)
            data.extend(f.readlines())

            if f.tell() == 0:
                break

        if len(data) > lines:
            data = data[-lines:]

    return data
