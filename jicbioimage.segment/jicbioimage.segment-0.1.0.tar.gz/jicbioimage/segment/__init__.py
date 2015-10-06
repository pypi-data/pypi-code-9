"""Module containing image segmentation functions.

Example usage:

>>> import numpy as np
>>> from jicbioimage.core.image import Image
>>> ar = np.array([[1, 1, 0, 0, 0],
...                [1, 1, 0, 0, 0],
...                [0, 0, 0, 0, 0],
...                [0, 0, 2, 2, 2],
...                [0, 0, 2, 2, 2]], dtype=np.uint8)
...
>>> im = Image.from_array(ar)
>>> connected_components(im)  # doctest: +NORMALIZE_WHITESPACE
SegmentedImage([[3, 3, 1, 1, 1],
                [3, 3, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 2, 2, 2],
                [1, 1, 2, 2, 2]])
>>> connected_components(im, background=0)  # doctest: +NORMALIZE_WHITESPACE
SegmentedImage([[2, 2, 0, 0, 0],
                [2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 1, 1, 1]])
>>> segmentation = connected_components(im, background=0)
>>> segmentation.history
['Created image from array', 'Applied connected_components transform']

"""

import numpy as np
import skimage.measure
import skimage.morphology

from jicbioimage.core.image import SegmentedImage
from jicbioimage.core.transform import transformation

__version__ = "0.1.0"


@transformation
def connected_components(image, connectivity=2, background=None):
    """Return :class:`jicbioimage.core.image.SegmentedImage`.

    :param image: input :class:`jicbioimage.core.image.Image`
    :param connectivity: maximum number of orthagonal hops to consider a
                         pixel/voxel as a neighbor
    :param background: consider all pixels with this value (int) as background
    :returns: :class:`jicbioimage.core.image.SegmentedImage`
    """
    ar = skimage.measure.label(image, connectivity=connectivity,
                               background=background)

    # The :class:`jicbioimage.core.image.SegmentedImage` assumes that zero is
    # background.  So we need to change the identifier of any pixels that are
    # marked as zero if there is no background in the input image.
    if background is None:
        ar[np.where(ar == 0)] = np.max(ar) + 1
    else:
        if np.min(ar) == -1:
            # Work around skimage.measure.label behaviour pre version 0.12.
            # Pre version 0.12 the background in skimage was labeled -1 and the
            # first component was labelled with 0.
            # The jicbioimage.core.image.SegmentedImage assumes that the
            # background is labelled 0.
            ar[np.where(ar == 0)] = np.max(ar) + 1
            ar[np.where(ar == -1)] = 0

    segmentation = SegmentedImage.from_array(ar)
    return segmentation


@transformation
def watershed_with_seeds(image, seeds, mask=None):
    """Return :class:`jicbioimage.core.image.SegmentedImage`.

    :param image: input :class:`jicbioimage.core.image.Image`
    :param seeds: numpy.ndarray of same shape as image,
                  each seed needs to be a unique integer
    :param mask: bool numpy.ndarray of same shape as image,
                 only regions that are marked as True will be labelled
    :returns: :class:`jicbioimage.core.image.SegmentedImage`
    """
    ar = skimage.morphology.watershed(-image, seeds, mask=mask)
    segmentation = SegmentedImage.from_array(ar)
    return segmentation
