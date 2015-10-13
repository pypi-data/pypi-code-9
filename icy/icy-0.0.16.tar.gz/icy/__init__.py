from importlib.util import find_spec

from .icy import preview
from .icy import read
from .icy import mem
from .icy import merge
from .icy import _path_to_objs
from .icy import run_examples

import icy.utils

ml_deps = [(p, find_spec(p)) for p in ['sklearn', 'xgboost', 'scipy', 'tables']]
if all([e[1] for e in ml_deps]):
    import icy.ml.crossval
    import icy.ml.explore
    import icy.ml.features
    import icy.ml.metrics
    import icy.ml.persist
    import icy.ml.prep
else:
    print('WARNING: dependencies {} for icy.ml missing, subpackage not available'.format( \
        ', '.join([e[0] for e in ml_deps if not e[1]])))

__version__ = '0.0.16'