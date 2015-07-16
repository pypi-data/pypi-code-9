import logging
logger=logging.getLogger(__name__)

import os
import matplotlib.pyplot as plt

def savefig(filename,path="figs",fig=None,ext='eps',**kwargs):
    filename       = os.path.join(path,filename)
    final_filename = '{}.{}'.format(filename,ext).replace(" ","").replace("\n","")
    final_filename = os.path.abspath(final_filename)

    final_path = os.path.dirname(final_filename)
    if not os.path.exists(final_path):
        os.makedirs(final_path)

    if fig != None:
        fig.savefig(final_filename,bbox_inches='tight',**kwargs)
    else:
        plt.savefig(final_filename,bbox_inches='tight',**kwargs)
