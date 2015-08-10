from __future__ import print_function, division
from os.path import join
import matplotlib.pyplot as plt
from ciabatta import ejm_rcparams
import numpy as np
from glob import glob
from ahoy.utils import utils

save_flag = False

use_latex = save_flag
use_pgf = True

ejm_rcparams.set_pretty_plots(use_latex, use_pgf)

fig = plt.figure(figsize=(12, 12 * ejm_rcparams.golden_ratio))
ax = fig.add_subplot(111)
ejm_rcparams.prettify_axes(ax)

cs = iter(ejm_rcparams.set2)

dirname = '/Users/ewj/Desktop/ahoy/data/pore_drift_pf_scan_L_300'

dirname_sets = [
    ['Tumble, Two-sided, Spatial', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),p=1,chi=*,side=2,type=S,turn=align,pore_R=30,pf=*,period=True'))],
    ['Tumble, Two-sided, Temporal', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),p=1,chi=*,side=2,type=T,dtMem=0.1,tMem=5,turn=align,pore_R=30,pf=*,period=True'))],
    ['Rotate, Two-sided, Spatial', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),Dr=1,chi=*,side=2,type=S,turn=align,pore_R=30,pf=*,period=True'))],
    ['Rotate, Two-sided, Temporal', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),Dr=1,chi=*,side=2,type=T,dtMem=0.1,tMem=5,turn=align,pore_R=30,pf=*,period=True'))],

    ['Tumble, One-sided, Spatial', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),p=1,chi=*,side=1,type=S,turn=align,pore_R=30,pf=*,period=True'))],
    ['Tumble, One-sided, Temporal', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),p=1,chi=*,side=1,type=T,dtMem=0.1,tMem=5,turn=align,pore_R=30,pf=*,period=True'))],
    ['Rotate, One-sided, Spatial', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),Dr=1,chi=*,side=1,type=S,turn=align,pore_R=30,pf=*,period=True'))],
    ['Rotate, One-sided, Temporal', glob(join(dirname, 'ships_2D,dt=0.01,n=5000,align=0,origin=0,v=20,L=(300.0, 300.0),Dr=1,chi=*,side=1,type=T,dtMem=0.1,tMem=5,turn=align,pore_R=30,pf=*,period=True'))],
]

ax.set_xlim(-0.02, 1.0)
ax.set_ylim(0.0, 0.205)

for label, dirnames in dirname_sets:
    pfs, uds = utils.pf_uds_x(dirnames)
    i_sort = np.argsort(pfs)
    pfs, uds = pfs[i_sort], uds[i_sort]
    ax.plot(pfs, uds, label=label)

ax.legend(loc='lower right', fontsize=26)
ax.set_xlabel(r'$\phi$', fontsize=35)
ax.set_ylabel(r'$\mathrm{v}_{d} / \mathrm{v}$', fontsize=35)
ax.tick_params(axis='both', labelsize=26, pad=10.0)
# ax.set_xlim(0.0, 16.0)
# ax.set_ylim(0.0, 1.01)

if save_flag:
    plt.savefig('plots/chi_k_2d.pdf', bbox_inches='tight')
else:
    plt.show()
