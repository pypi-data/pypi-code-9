#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import json
from .settings import SERVER_HOST, SERVER_PORT

import logging
logger = logging.getLogger('graphalviz.client')


def recv_basic(sock):
    total_data = []
    while True:
        data = sock.recv(1024)
        if not data:
            break
        total_data.append(data)
    return ''.join(total_data)


def send(data, ip=SERVER_HOST, port=SERVER_PORT):
    """ GraphAlViz client example """
    # Utworz socket (SOCK_STREAM określa socket TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    received = ''

    try:
        # Polacz się z serwerem i przeslij dane
        sock.sendall(bytes(data))
        logger.debug("Sending [%s:%s]: %s", ip, port, data)
        # Odbierz dane z serwera i zamknij klienta
        received = recv_basic(sock)
        logger.debug("Received: %s", received)
    finally:
        sock.close()
    return received


class GraphAlVizSimpleClient(object):
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port

    def set_positioning_algorithm(self, alg):
        """
        """
        send("set_positioning_algorithm('{}')".format(alg),
             self.host, self.port)

    def load(self, file_name):
        """
        """
        # TODO: Add description
        send("load('{}')".format(file_name), self.host, self.port)

    def plot(self):
        """
        """
        # TODO: Add description
        send("plot()", self.host, self.port)

    def close_plot(self):
        """
        """
        # TODO: Add description
        send("close_plot()", self.host, self.port)

    def edges(self):
        """
        """
        # TODO: Add description
        response = send(
            "edges()",
            self.host, self.port
        )
        return json.loads(response)

    def vertices(self):
        """
        """
        # TODO: Add description
        response = send(
            "vertices()",
            self.host, self.port
        )
        return json.loads(response)

    def neighbors(self, vertex_no):
        """
        """
        # TODO: Add description
        response = send(
            "neighbors({})".format(vertex_no),
            self.host, self.port
        )
        return json.loads(response)

    def get_v_color(self, vertex_no):
        """
        """
        # TODO: Add description
        response = send(
            "get_v_color({})".format(vertex_no),
            self.host, self.port
        )
        return json.loads(response)

    def set_v_color(self, vertex_no, color):
        """
        """
        # TODO: Add description
        response = send(
            "set_v_color({},{})".format(vertex_no, color),
            self.host, self.port
        )
        return json.loads(response)

    def get_e_color(self, vertex_no_1, vertex_no_2):
        """
        """
        # TODO: Add description
        response = send(
            "get_e_color({},{})".format(vertex_no_1, vertex_no_2),
            self.host, self.port
        )
        return json.loads(response)

    def set_e_color(self, vertex_no_1, vertex_no_2, color):
        """
        """
        # TODO: Add description
        send(
            "set_e_color({},{},{})".format(vertex_no_1, vertex_no_2, color),
            self.host, self.port
        )

    def set_label_v(self, vertex_no, label):
        """
        """
        # TODO: Add description
        send(
            "set_label_v({},{})".format(vertex_no, label),
            self.host, self.port
        )

    def set_label_e(self, vertex_no_1, vertex_no_2, label):
        """
        """
        # TODO: Add description
        send(
            "set_label_e({},{},{})".format(vertex_no_1, vertex_no_2, label),
            self.host, self.port
        )
