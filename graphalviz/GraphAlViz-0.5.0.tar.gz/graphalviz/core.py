# -*- coding: utf-8 -*-
import networkx as nx
from .tools import num, nonblank_lines

import logging
logger = logging.getLogger('graphalviz.core')


def normalize_value(value):
    """
    Normalizacja wartosci do przedziału 0-1
    """
    return 1.0 / (1.0 + abs(value))


def number_of_intersections(data):
    """
    Obliczenie ilosci punktów przecięcia odcinków
    """
    # calculate number of cross points
    result = 0

    for i in range(len(data) - 1):
        v1 = data[i]
        a1 = (v1[1] - v1[3]) * 1.0 / (v1[0] - v1[2]) if v1[0] != v1[2] else 0
        b1 = v1[1] - a1 * v1[0]
        for j in range(i + 1, len(data)):
            v2 = data[j]
            a2 = (v2[1] - v2[3]) * 1.0 / (v2[0] - v2[2]) if v2[0] != v2[2] else 0
            b2 = v2[1] - a2 * v2[0]
            if a1 != a2:
                x = (b2 - b1) * 1.0 / (a1 - a2)
                y = a1 * x + b1
                if (
                    x > min(v1[0], v1[2]) and
                    x < max(v1[0], v1[2]) and
                    x > min(v2[0], v2[2]) and
                    x < max(v2[0], v2[2]) and
                    y > min(v1[1], v1[3]) and
                    y < max(v1[1], v1[3]) and
                    y > min(v2[1], v2[3]) and
                    y < max(v2[1], v2[3])
                ):
                    result += 1

            elif b1 == b2:
                # TODO: add aditionall check if the edges overlap
                # add line overlapping penalty
                result += 1000

    return normalize_value(result)


def edge_lenght_variation(data):
    """
    Obliczenie odchylenia standardowego dlugosci krawedzi
    """
    import numpy as np

    m = np.array(data)
    norm = np.linalg.norm(m[:, 2:4] - m[:, 0:2], axis=1)

    result = np.std(norm)

    return normalize_value(result)


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
    DEFAULT_POSITIONING = 'optimal'
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
                'iterations': 200,
            },
        },
    }
    BEST_POSITIONING_FUNCTION = {
        'algorithms': {
            'circular_layout': {
                'iterations': 1,
                'options': {},
            },
            'shell_layout': {
                'iterations': 1,
                'options': {},
            },
            'spectral_layout': {
                'iterations': 1,
                'options': {},
            },
            'spring_layout': {
                'iterations': 10,
                'options': {
                    'iterations': 200,
                },
            },
        },
    }

    def __init__(self, **kwargs):
        """Inicjalizacja grafu

        :nazwa_pliku: nazwa pliku lub pełna ścieżka do pliku zawierającego graf

        """
        self._refresh_on_change = kwargs.get('refresh_on_change', False)
        self._file_name = kwargs.get('file_name', None)
        self._positions = None
        self._loaded = False
        self._rating_functions = kwargs.get(
            'rating_functions',
            [number_of_intersections, edge_lenght_variation]
        )
        self._load_from_file()
        if not hasattr(self, '_typ_grafu'):
            self._initialize_graph(kwargs.get('graph_type', self.UNDIRECTED))
        self.positioning_algorithm = kwargs.get(
            'positioning', self.DEFAULT_POSITIONING)

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
        if val in self.POSITIONING_ALGORITHMS or val == 'optimal':
            self._positioning = val
            self._positions = None
            logger.debug(
                'Graph vertices positioning algorithm set to: %s',
                self._positioning
            )

    def set_positioning_algorithm(self, val, options={}):
        """
        """
        self.positioning_algorithm = val
        if (
            options and
            val in self.POSITIONING_ALGORITHMS and
            'options' in self.POSITIONING_ALGORITHMS[val]
        ):
            self.POSITIONING_ALGORITHMS[val]['options'].update(options)
        self._conditional_refresh()

    def _initialize_graph(self, graph_type=UNDIRECTED):
        # usun z pamieci graf jesli poprzednio zaladowany
        if getattr(self, '_graph', None):
            del self._graph

        if getattr(self, '_weighted_graph', None):
            del self._weighted_graph

        self._graph_type = graph_type
        # zainicjuj graf w zaleznosci od typu
        if self._graph_type:
            self._graph = nx.MultiDiGraph(graph_type=self.DIRECTED)
            self._weighted_graph = nx.MultiDiGraph(graph_type=self.DIRECTED)
        else:
            self._graph = nx.MultiGraph(graph_type=self.UNDIRECTED)
            self._weighted_graph = nx.MultiGraph(graph_type=self.UNDIRECTED)

        self._loaded = False

        logger.debug('Graph initialized, type: %s', self._graph_type)

    def _load_from_file(self):
        """Odczytuja strukture grafu z pliku"""

        # Brak zdefiniowanej nazwy pliku
        if not self._file_name:
            # TODO: zaimplementowac obsluge bledu
            return

        # otworz i odczytaj plik

        with open(self._file_name, 'Ur') as f:
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
            for line in nonblank_lines(f):
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
                    weight=1
                )
                self._weighted_graph.add_edge(
                    edge_no_1,
                    edge_no_2,
                    weight=weight
                )
        self._loaded = True
        if vertex_count != self.vertex_count:
            logger.error('Wrong number of vertices in the file %s! Declared %s, defined %s',
                         self._file_name, vertex_count, self.vertex_count)
            self._loaded = False
        if edge_count != self.edge_count:
            logger.error('Wrong number of edges in the file %s! Declared %s, defined %s',
                         self._file_name, edge_count, self.edge_count)
            self._loaded = False
        if not self._loaded:
            self._initialize_graph(graph_type)
        logger.debug(
            'Graph vertices and edges loaded from file: %s', self._file_name)

    def _get_positions(self):
        """
        Wyznacz pozycje wierzcholkow
        """
        if self.edge_count > 0:
            # check if positioning should be optimal
            if self._positioning == 'optimal':
                self._positions = self.get_optimal_positions()
            else:
                # if not optimal do a dedicated positioning
                positioning = getattr(
                    nx, self._positioning, getattr(nx, 'random_layout'))
                kwargs = self.POSITIONING_ALGORITHMS.get(
                    self._positioning, {}).get('options', {})
                self._positions = positioning(self._graph, **kwargs)
            logger.debug('Graph new vertices position calculated')
            return self._positions

    def get_optimal_positions(self):
        """
        Wyznacz optymalne pozycje wierzcholow
        """
        alg = ''
        ratings = [-1 for i in self._rating_functions]
        for pos_alg in self.BEST_POSITIONING_FUNCTION.get('algorithms', {}).keys():
            for alg_iter in range(self.BEST_POSITIONING_FUNCTION['algorithms'][pos_alg].get('iterations', 1)):
                positioning = getattr(
                    nx, pos_alg, getattr(nx, 'random_layout'))
                kwargs = self.BEST_POSITIONING_FUNCTION['algorithms'][pos_alg].get('options', {})
                pos = positioning(self._graph, **kwargs)
                current_rating = []
                # convert to matrixes
                pos_m = []
                for edge in self._graph.edges():
                    pos_m.append([
                        pos[edge[0]][0], pos[edge[0]][1],
                        pos[edge[1]][0], pos[edge[1]][1]
                    ])

                # calculate rating
                for rating_fun in self._rating_functions:
                    current_rating.append(rating_fun(pos_m))
                if current_rating > ratings:
                    alg = pos_alg
                    self._positions = pos
                    ratings = current_rating
        logger.debug(
            'Graph vertices optimal positions calculated, algorithm: '
            '%s, result: %s', alg, ratings)
        return self._positions

    def _write_to_file(self):
        """
        Zapisz pozycje wierzcholkow
        """
        if not self._positions:
            self._get_positions()

        if not self._file_name or not self._positions:
            # TODO: zaimplementowac obsluge bledu
            logger.warning('Could not write to file. Either data is missing or no file name')
            return

        # otworz plik do zapisu
        with open(self._file_name, 'a') as f:
            f.write('## Vertex positions [{}] ##\n'.format(
                self._positioning))
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
        return True

    def _conditional_refresh(self):
        """
        """
        if self._refresh_on_change:
            self.plot()

    def plot(self):
        """
        """
        import matplotlib
        matplotlib.use('TkAgg')
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            logger.warning(
                'The matplotlib library or some part of it is not present. '
                + str(e)
            )
            return
        plt.ion()
        # wyczysc okno
        plt.figure(
            1,
            facecolor='white',
            edgecolor='white',
            frameon=False,
            tight_layout=True
        )
        plt.clf()
        plt.show()

        plt.gca().set_xticklabels([])
        plt.gca().set_yticklabels([])

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
            node_size=500,
            alpha=1.0)

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

        plt.draw()
        logger.debug('Graph ploted')
        return True

    def close_plot(self):
        """
        """
        import matplotlib
        matplotlib.use('TkAgg')
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            logger.warning(
                'The matplotlib library or some part of it is not present. '
                + str(e)
            )
            return
        plt.ion()
        plt.close()
        return True

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
        return True

    def load(self, file_name):
        """
        """
        self.load_only(file_name)
        self._get_positions()
        self._write_to_file()
        self._conditional_refresh()
        return True

    def edges(self):
        """
        """
        return self._graph.edges()

    def edges_iter(self):
        """
        """
        return self._graph.edges_iter()

    def vertices(self):
        """
        """
        return self._graph.nodes()

    def vertices_iter(self):
        """
        """
        return self._graph.nodes_iter()

    def neighbors(self, vertex_no):
        """
        """
        vertex_no = int(vertex_no)
        return self._graph.neighbors(vertex_no)

    def neighbors_iter(self, vertex_no):
        """
        """
        vertex_no = int(vertex_no)
        return self._graph.neighbors_iter(vertex_no)

    def get_v_color(self, vertex_no):
        """
        """
        vertex_no = int(vertex_no)
        return self._graph.node[vertex_no].get('color', '')

    def set_v_color(self, vertex_no, color):
        """
        """
        vertex_no = int(vertex_no)
        color = self._get_color(color, self.DEFAULT_VERTEX_COLOR)
        self._graph.node[vertex_no]['color'] = color
        logger.debug('Graph vertex: %s color set to: %s', vertex_no, color)
        self._conditional_refresh()
        return True

    def get_e_color(self, vertex_no_1, vertex_no_2):
        """
        """
        vertex_no_1 = int(vertex_no_1)
        vertex_no_2 = int(vertex_no_2)
        return self._graph.edge[vertex_no_1][vertex_no_2][0].get('color', '')

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
        self._conditional_refresh()
        return True

    def set_label_v(self, vertex_no, label):
        """
        """
        self._graph.node[int(vertex_no)]['label'] = label
        logger.debug('Graph vertex: %s label set to: %s', vertex_no, label)
        self._conditional_refresh()
        return True

    def set_label_e(self, vertex_no_1, vertex_no_2, label):
        """
        """
        self._graph.edge[int(vertex_no_1)][int(vertex_no_2)][0]['label'] = label
        logger.debug(
            'Graph edge: %s-%s label set to: %s',
            vertex_no_1, vertex_no_2, label)
        self._conditional_refresh()
        return True
