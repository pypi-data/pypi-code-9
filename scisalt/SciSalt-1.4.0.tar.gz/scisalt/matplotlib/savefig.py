import logging
logger = logging.getLogger(__name__)

import os
import sys
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.pyplot as plt


def savefig(filename, path="figs", fig=None, ext='eps', **kwargs):
    """
    Save the figure *fig* (optional, if not specified, latest figure in focus) to *filename* in the path *path* with extension *ext*.

    *\*\*kwargs* is passed to :meth:`matplotlib.figure.Figure.savefig`.
    """
    filename       = os.path.join(path, filename)
    final_filename = '{}.{}'.format(filename, ext).replace(" ", "").replace("\n", "")
    final_filename = os.path.abspath(final_filename)

    final_path = os.path.dirname(final_filename)
    if not os.path.exists(final_path):
        os.makedirs(final_path)

    if fig is not None:
        fig.savefig(final_filename, bbox_inches='tight', **kwargs)
    else:
        plt.savefig(final_filename, bbox_inches='tight', **kwargs)
