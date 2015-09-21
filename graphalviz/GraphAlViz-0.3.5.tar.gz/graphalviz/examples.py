# standardowe wykorzystanie biblioteki graphalviz
from graphalviz.core import GraphAlViz
import os

demo_graph = GraphAlViz()

directory = os.path.realpath(os.path.dirname(__file__))
file_name = os.path.join(directory, 'graph_example')
demo_graph.load_only(file_name)
demo_graph.plot()

# graf z rozlokowaniem w oparciu o metode circular
demo_graph.positioning_algorithm = 'circular_layout'
demo_graph.plot()

# graf z rozlokowaniem w oparciu o metode random
demo_graph.positioning_algorithm = 'random_layout'
demo_graph.plot()

# graf z rozlokowaniem w oparciu o metode shell
demo_graph.positioning_algorithm = 'shell_layout'
demo_graph.plot()

# graf z rozlokowaniem w oparciu o metode spectral
demo_graph.positioning_algorithm = 'spectral_layout'
demo_graph.plot()

# graf z rozlokowaniem w oparciu o metode springs
demo_graph.positioning_algorithm = 'springs_layout'
demo_graph.plot()

# graf z optymalnym rozlokowaniem
# TODO: napisac


# standardowe wykorzystanie biblioteki w architekturze klient/serwer
# TODO: napisac
