import ipdb                              # noqa
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as _np
import logging

from matplotlib.backends.backend_pdf import PdfPages

logger = logging.getLogger(__name__)


def imshow_batch(images, cbar=True, show=True, pdf=None, figsize=(16, 12), title=None, rows=2, columns=2, cmap=None, **kwargs):
    # ======================================
    # Set up grid
    # ======================================
    images = _np.array(images)
    gs = gridspec.GridSpec(rows, columns)

    num_imgs = images.shape[0]
    max_ind = num_imgs-1

    # ======================================
    # Split into pages
    # ======================================
    per_page = rows*columns
    num_pages = _np.int(_np.ceil(num_imgs/per_page))
    fig_array = _np.empty(shape=num_pages, dtype=object)

    if num_pages > 1:
        logger.info('Multiple pages necessary')

    if pdf is not None:
        f = PdfPages(pdf)

    for p in range(num_pages):
        # ======================================
        # Make figure
        # ======================================
        fig_array[p] = plt.figure(figsize=figsize)

        # ======================================
        # Get number of rows on page
        # ======================================
        pg_max_ind = _np.min( [(p+1) * per_page - 1, max_ind] )
        num_rows = _np.int(_np.ceil((pg_max_ind+1 - p * per_page) / columns))

        for i in range(num_rows):
            # ======================================
            # Get images for column
            # ======================================
            i_min_ind = p * per_page + i * columns
            col_max_ind = _np.min([i_min_ind + columns - 1, max_ind])
            
            for j, image in enumerate(images[i_min_ind:col_max_ind+1]):
                ax = fig_array[p].add_subplot(gs[i, j])

                try:
                    if _np.issubdtype(image.dtype, _np.integer):
                        image = _np.array(image, dtype=float)
                except:
                    pass

                plot = ax.imshow(image, **kwargs)
                if cmap is not None:
                    plot.set_cmap(cmap)

                if cbar:
                    fig_array[p].colorbar(plot)

        fig_array[p].tight_layout()
        if pdf is not None:
            f.savefig(fig_array[p])

        if not show:
            plt.close(fig_array[p])

    if pdf is not None:
        f.close()

    return fig_array
