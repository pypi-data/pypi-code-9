import scipy as sp
from collections import namedtuple
import scipy.ndimage as spim
import skimage as skim
from skimage import morphology


class MedialAxisThinning(object):
    r"""

    """

    def __init__(self, image):
        super().__init__()
        image = sp.atleast_3d(image)
        self.image = sp.array(image, dtype=bool)

    def run(self):
        r"""


        """
        imtemp = morphology.medial_axis(self.image)
