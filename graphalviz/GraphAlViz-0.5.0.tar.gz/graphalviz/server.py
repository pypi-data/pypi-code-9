# -*- coding: utf-8 -*-
import SocketServer
import json
from .core import GraphAlViz
from .settings import SERVER_HOST, SERVER_PORT

import logging
logger = logging.getLogger('graphalviz.server')


class GraphAlVizTCPServer(SocketServer.TCPServer):
    def __init__(self, *args, **kwargs):
        self.graph = GraphAlViz(
            refresh_on_change=kwargs.pop('refresh_on_change', False)
        )
        SocketServer.TCPServer.__init__(self, *args, **kwargs)


class GraphAlVizTCPHandler(SocketServer.BaseRequestHandler):
    """
    RequestHandler serwera

    Inicjalizowany raz na polacznie z serwerem. Powinno przeciazac metode
    handle() by implementowac komunikacje z klientem.
    """

    def handle(self):
        result = ''
        # self.request to socket TCP polaczony z klientem
        self.data = self.request.recv(1024).strip()
        logger.debug(
            "Received [%s]: %s", self.client_address[0], self.data)
        # wywolaj odpowiednia funkcje
        fun = getattr(self.server.graph, self.data.split('(')[0].strip(), None)
        if fun:
            # wytnij czesc z atrybutami
            atr = self.data[
                self.data.find('(') + 1:self.data.rfind(')')
            ].strip()
            if atr:
                # usun cudzyslowy i podziel na parametry
                atr = atr.replace('"', '').replace("'", '').split(',')
                logger.debug(
                    "Running %s with %s parameters", fun.__name__, atr)
                result = fun(*atr)
            else:
                logger.debug("Running %s", fun.__name__)
                result = fun()
        # przeslij informacje zwrotna - np. czy poprawnie przetworzono dane
        # przeslane z klienta
        self.request.sendall(json.dumps(result))


def main(host=SERVER_HOST, port=SERVER_PORT, refresh_on_change=False):
    # TODO: dodaj opis
    """
    """
    # Utworz server, przypisujac do HOST'a na porcie PORT
    server = GraphAlVizTCPServer(
        (host, port),
        GraphAlVizTCPHandler,
        refresh_on_change=refresh_on_change
    )
    logger.info('Staring GraphAlViz server on %s:%s ...', host, port)

    # Aktywacja serwera. Serwer bedzie dzialal caly czas do momentu wcisniecia
    # Ctrl-C
    server.serve_forever()
    logger.info('Stoping GraphAlViz server ...')
