# -*- coding: utf-8 -*-
import SocketServer
from .core import GraphAlViz
from .settings import SERVER_HOST, SERVER_PORT

import logging
logger = logging.getLogger('graphalviz.server')


# TODO: change it to local variable of main function
graph = GraphAlViz()


class GraphAlVizTCPHandler(SocketServer.BaseRequestHandler):
    """
    RequestHandler serwera

    Inicjalizowany raz na polacznie z serwerem. Powinno przeciazac metode
    handle() by implementowac komunikacje z klientem.
    """
    graph = graph

    # TODO: implement it with graph as input variable
    # def __init__(self, *args, **kwargs):
    #     self._graph = graph
    #     SocketServer.BaseRequestHandler.__init__(*args, **kwargs)

    def handle(self):
        # self.request to socket TCP polaczony z klientem
        self.data = self.request.recv(1024).strip()
        logger.debug(
            "Received [%s]: %s", self.client_address[0], self.data)
        # wywolaj odpowiednia funkcje
        fun = getattr(self.graph, self.data.split('(')[0].strip(), None)
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
                fun(*atr)
            else:
                logger.debug("Running %s", fun.__name__)
                fun()
        # przeslij informacje zwrotna - np. czy poprawnie przetworzono dane
        # przeslane z klienta
        result = 'OK'
        self.request.sendall(result)


def main(host=SERVER_HOST, port=SERVER_PORT):
    # TODO: dodaj opis
    """
    """
    # Utworz server, przypisujac do HOST'a na porcie PORT
    server = SocketServer.TCPServer((host, port), GraphAlVizTCPHandler)
    logger.info('Staring GraphAlViz server on %s:%s ...', host, port)

    # Aktywacja serwera. Serwer bedzie dzialal caly czas do momentu wcisniecia
    # Ctrl-C
    server.serve_forever()
    logger.info('Stoping GraphAlViz server ...')
