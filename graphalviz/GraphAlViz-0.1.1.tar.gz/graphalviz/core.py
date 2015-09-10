# -*- coding: utf-8 -*-
import networkx as nx
from .tools import num

import logging
logger = logging.getLogger('graphalviz.core')


class GraphAlViz(object):

    """Rysowanie grafów"""
    UNDIRECTED = 0
    DIRECTED = 1
    GRAPH_TYPES = {
        UNDIRECTED: 'Undirected',
        DIRECTED: 'Directed'
    }
    COLORS = {
        0: 'k',     # k - black
        1: 'b',     # b - blue
        2: 'g',     # g - green
        3: 'r',     # r - red
        4: 'c',     # c - cyan
        5: 'm',     # m - magenta
        6: 'y',     # y - yellow
        7: 'w',     # w - white
    }
    DEFAULT_VERTEX_COLOR = 'r'
    DEFAULT_EDGE_COLOR = 'k'
    DEFAULT_COLOR = 'k'
    DEFAULT_POSITIONING = 'random_layout'
    POSITIONING_ALGORITHMS = {
        'circular_layout': {
            'name': 'Circular layout',
        },
        'random_layout': {
            'name': 'Random layout',
        },
        'shell_layout': {
            'name': 'Shell layout',
        },
        'spectral_layout': {
            'name': 'Spectral layout',
        },
        'spring_layout': {
            'name': 'Spring layout',
            'options': {
                'iterations': 50,
            },
        },
    }

    def __init__(self, file_name=None, graph_type=UNDIRECTED, **kwargs):
        """Inicjalizacja grafu

        :nazwa_pliku: nazwa pliku lub pełna ścieżka do pliku zawierającego graf

        """
        self._file_name = file_name
        self._positions = None
        self._load_from_file()
        if not hasattr(self, '_typ_grafu'):
            self._initialize_graph(graph_type)
        self._positioning = kwargs.get(
            'positioning', self.DEFAULT_POSITIONING)
        if self._positioning not in [x for x in self.POSITIONING_ALGORITHMS.keys()]:
            self._positioning = self.DEFAULT_POSITIONING

    @property
    def edge_count(self):
        """
        """
        return self._graph.size()

    @property
    def vertex_count(self):
        """
        """
        return self._graph.order()

    @property
    def positioning_algorithm(self):
        """
        """
        return self._positioning

    @positioning_algorithm.setter
    def positioning_algorithm(self, val):
        if val in self.POSITIONING_ALGORITHMS:
            self._positioning = val
            self._positions = None
            logger.debug(
                'Graph vertices positioning algorithm set to: %s',
                self._positioning
            )

    def set_positioning_algorithm(self, val):
        """
        """
        self.positioning_algorithm = val

    def _initialize_graph(self, graph_type=UNDIRECTED):
        # usun z pamieci graf jesli poprzednio zaladowany
        if getattr(self, '_graph', None):
            del self._graph

        self._graph_type = graph_type
        # zainicjuj graf w zaleznosci od typu
        if self._graph_type:
            self._graph = nx.MultiDiGraph(graph_type=self.DIRECTED)
        else:
            self._graph = nx.MultiGraph(graph_type=self.UNDIRECTED)
        logger.debug('Graph initialized, type: %s', self._graph_type)

    def _load_from_file(self):
        """Odczytuja strukture grafu z pliku"""

        # Brak zdefiniowanej nazwy pliku
        if not self._file_name:
            # TODO: zaimplementowac obsluge bledu
            return

        # otworz i odczytaj plik

        with open(self._file_name, 'r') as f:
            # odczytaj typ grafu
            graph_type = num(f.readline().split('=')[1])
            self._initialize_graph(graph_type)

            # odczytaj liczbe wierzcholkow
            # TODO: niepotrzebne, moze byc wyznaczone po wczytaniu grafu, do
            # usuniecia po konsultacji
            vertex_count = num(f.readline().split('=')[1])

            # odczytaj liczbe krawedzi
            # TODO: niepotrzebne, moze byc wyznaczone po wczytaniu grafu, do
            # usuniecia po konsultacji
            edge_count = num(f.readline().split('=')[1])

            # czytaj opis grafu - lista krawedzi w formacie:
            # <nr wierzcholka> <nr wierzcholka> [<waga>]
            for line in f:
                # pomin komentarze i pozycje zapisane w pliku
                if line.lstrip()[0] == '#':
                    continue
                edge = line.split()
                # TODO: zabezpieczyc jesli nie ma krawedzi lub niepoprawny
                # format
                # kowertuj do liczby
                edge_no_1 = num(edge[0])
                edge_no_2 = num(edge[1])

                # konwertuj wage do liczby, domyslna waga = 1
                weight = num(edge[2]) if len(edge) == 3 else 1

                # dodaj krawedz do grafu
                self._graph.add_edge(
                    edge_no_1,
                    edge_no_2,
                    weight=weight
                )
        logger.debug(
            'Graph vertices and edges loaded from file: %s', self._file_name)

    def _get_positions(self):
        """
        Wyznacz pozycje wierzcholkow
        """
        positioning = getattr(
            nx, self._positioning, getattr(nx, self.DEFAULT_POSITIONING))
        kwargs = self.POSITIONING_ALGORITHMS.get(
            self._positioning, {}).get('options', {})
        self._positions = positioning(self._graph, **kwargs)
        logger.debug('Graph new vertices position calculated')
        return self._positions

    def _write_to_file(self):
        """
        Zapisz pozycje wierzcholkow
        """
        if not self._positions:
            self._get_positions()

        if not self._file_name:
            # TODO: zaimplementowac obsluge bledu
            return

        # otworz plik do zapisu
        with open(self._file_name, 'a') as f:
            f.write('## Vertex positions [{}] ##\n'.format(
                self.POSITIONING_ALGORITHMS.get(self._positioning, {}).get(
                    'name', 'unknown')))
            for pos in self._positions:
                # TODO: zabezpieczyc jesli pozycje juz istnieja - np. usunac
                # stare
                f.write(
                    '#{0} ({1:03.2f}, {2:03.2f})\n'.format(
                        pos, self._positions[pos][0], self._positions[pos][1]
                    )
                )
        logger.debug(
            'Graph vertices position writen to file: %s', self._file_name)

    def clear_positions(self):
        """
        Wyczysc pozycje wierzcholkow
        """
        self._positions = None
        logger.debug('Graph vertices position cleaned')

    def plot(self):
        """
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            logger.warning(
                'The matplotlib library or some part of it is not present. '
                + str(e)
            )
            return
        # wyczysc okno
        plt.clf()
        plt.close()

        # FIXME: make plots interactive
        #plt.ion()

        # pozycje wierzcholkow
        if not self._positions:
            self._get_positions()
        pos = self._positions

        # wierzcholki
        nx.draw_networkx_nodes(
            self._graph,
            pos,
            node_color=[
                self._graph.node[i].get('color', self.DEFAULT_VERTEX_COLOR)
                for i in self._graph.nodes()
            ],
            #label=['' for i in self._graf.nodes()],
            node_size=1000,
            alpha=0.9)

        # krawedzie
        nx.draw_networkx_edges(
            self._graph,
            pos,
            edge_color=[
                self._graph.edge[i][j][0].get('color', self.DEFAULT_EDGE_COLOR)
                for i, j in self._graph.edges()],
            width=2.0,
            alpha=0.8)

        # etykiety wierzcholkow
        labels = {}
        for i in self._graph.nodes():
            if self._graph.node[i].get('label', ''):
                labels[i] = '{0} [{1}]'.format(
                    i, self._graph.node[i].get('label', ''))
            else:
                labels[i] = '{0}'.format(i)
        nx.draw_networkx_labels(
            self._graph,
            pos,
            labels,
            font_size=12,
            font_family='sans-serif'
        )

        # etykiety krawedzi
        edge_labels = {}
        for i, j in self._graph.edges():
            edge_labels[(i, j)] = '{0}'.format(
                self._graph.edge[i][j][0].get('label', ''))
        nx.draw_networkx_edge_labels(
            self._graph,
            pos,
            edge_labels,
            label_pos=0.4,
            font_size=10,
            font_family='sans-serif'
        )

        plt.gca().set_xticklabels([])
        plt.gca().set_yticklabels([])

        plt.show()
        logger.debug('Graph ploted')

    def _get_color(self, color, default_color=DEFAULT_COLOR):
        try:
            color = int(color)
        except ValueError:
            pass
        else:
            color = self.COLORS.get(color, default_color)
        return color

    def load_only(self, file_name):
        """
        """
        self._file_name = file_name
        self._load_from_file()

    def load(self, file_name):
        """
        """
        self.load_only(file_name)
        self._get_positions()
        self._write_to_file()

    def set_v_color(self, vertex_no, color):
        """
        """
        vertex_no = int(vertex_no)
        color = self._get_color(color, self.DEFAULT_VERTEX_COLOR)
        self._graph.node[vertex_no]['color'] = color
        logger.debug('Graph vertex: %s color set to: %s', vertex_no, color)

    def set_e_color(self, vertex_no_1, vertex_no_2, color):
        """
        """
        vertex_no_1 = int(vertex_no_1)
        vertex_no_2 = int(vertex_no_2)
        color = self._get_color(color, self.DEFAULT_EDGE_COLOR)
        self._graph.edge[vertex_no_1][vertex_no_2][0]['color'] = color
        logger.debug(
            'Graph edge: %s-%s color set to: %s',
            vertex_no_1, vertex_no_2, color)

    def set_label_v(self, vertex_no, label):
        """
        """
        self._graph.node[int(vertex_no)]['label'] = label
        logger.debug('Graph vertex: %s label set to: %s', vertex_no, label)

    def set_label_e(self, vertex_no_1, vertex_no_2, label):
        """
        """
        self._graph.edge[int(vertex_no_1)][int(vertex_no_2)][0]['label'] = label
        logger.debug(
            'Graph edge: %s-%s label set to: %s',
            vertex_no_1, vertex_no_2, label)
