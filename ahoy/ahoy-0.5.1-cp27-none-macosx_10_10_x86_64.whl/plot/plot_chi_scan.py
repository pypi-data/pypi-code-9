from __future__ import print_function, division
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from ahoy.utils import utils


dirnames_1D_p_1side_S = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_1D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=1,pType=S,noObs')
dirnames_1D_p_1side_T = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_1D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=1,pType=T,dtMem=0.1,ptMem=5,noObs')
dirnames_1D_p_2side_S = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_1D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=2,pType=S,noObs')
dirnames_1D_p_2side_T = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_1D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=2,pType=T,dtMem=0.1,ptMem=5,noObs')
dirnames_2D_Dr_1side_S = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,Dr=1,DChi=*,DSide=1,DType=S,noObs')
dirnames_2D_Dr_1side_T = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,Dr=1,DChi=*,DSide=1,DType=T,DtMem=5,noObs')
dirnames_2D_Dr_2side_S = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,Dr=1,DChi=*,DSide=2,DType=S,noObs')
dirnames_2D_Dr_2side_T = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,Dr=1,DChi=*,DSide=2,DType=T,DtMem=5,noObs')
dirnames_2D_p_1side_S = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=1,pType=S,noObs')
dirnames_2D_p_1side_T = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=1,pType=T,dtMem=0.1,ptMem=5,noObs')
dirnames_2D_p_2side_S = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=2,pType=S,noObs')
dirnames_2D_p_2side_T = glob('/Users/ewj/Desktop/ahoy_data/chi_scan/ships_2D,dt=0.01,n=1000,align=0,origin=1,v=1,p=1,pChi=*,pSide=2,pType=T,dtMem=0.1,ptMem=5,noObs')

dirname_sets = [
    # (dirnames_1D_p_1side_S, '1D_p_1side_S'),
    # (dirnames_1D_p_1side_T, '1D_p_1side_T'),
    # (dirnames_1D_p_2side_S, '1D_p_2side_S'),
    # (dirnames_1D_p_2side_T, '1D_p_2side_T'),
    (dirnames_2D_Dr_1side_S, '2D_Dr_1side_S'),
    (dirnames_2D_Dr_1side_T, '2D_Dr_1side_T'),
    (dirnames_2D_Dr_2side_S, '2D_Dr_2side_S'),
    (dirnames_2D_Dr_2side_T, '2D_Dr_2side_T'),
    (dirnames_2D_p_1side_S, '2D_p_1side_S'),
    (dirnames_2D_p_1side_T, '2D_p_1side_T'),
    (dirnames_2D_p_2side_S, '2D_p_2side_S'),
    (dirnames_2D_p_2side_T, '2D_p_2side_T'),
]

fig = plt.figure()
ax = fig.add_subplot(111)

chis_th = np.linspace(0.0, 0.95, 100)

uds_th_1d_p_2side_S = chis_th
uds_th_1d_p_1side_S = chis_th / (2.0 - chis_th)
uds_th_2d_p_2side_S = (1.0 - np.sqrt(1.0 - chis_th ** 2.0)) / chis_th

ax.plot(chis_th, uds_th_1d_p_2side_S, label='1D_p_2side_S theory')
ax.plot(chis_th, uds_th_1d_p_1side_S, label='1D_p_1side_S theory')
ax.plot(chis_th, uds_th_2d_p_2side_S, label='2D_p_2side_S theory')

ud_0 = 0.17

for dirnames, label in dirname_sets:
    chis, uds = utils.chi_uds_x(dirnames)
    i_sort = np.argsort(chis)
    chis, uds = chis[i_sort], uds[i_sort]
    ax.plot(chis, uds, label=label)
    chi_0 = utils.curve_intersect(chis, uds, ud_0)
    print(label, chi_0)

ax.set_xlim(-0.02, 1.0)
ax.set_ylim(0.0, 1.1)
ax.legend(loc='upper left')

plt.show()
