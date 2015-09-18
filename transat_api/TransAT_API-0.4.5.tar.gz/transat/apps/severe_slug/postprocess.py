from transat.postproc.postprocessing import Postprocessing
import os
import matplotlib.pyplot as plt
import numpy as np


def main(*args, **kargs):
    spp = Postprocessing()
    outputs = spp.pressure_drop(0, 10)
    return outputs


def plot_pressure(folder, points):
    print points
    #folder = os.path.join(folder, 'RESULT')
    #vtm = spp.pa.get_last_modified(folder)
    #spp = Postprocessing()
    #filter = spp.pa.pa.OpenDataFile(vtm)
    #pressure = np.array([])
    #for i in range(len(points) - 1):
    #    pnew = spp.pa.get_line_plot(filter, points[i], points[i + 1], cell=False)['P']
    #    print pnew
    #    pnew = pnew[~np.isnan(pnew)]
    #    pressure = np.concatenate((pressure, pnew))
    #plt.plot(pressure)
    #figure_name = os.path.join(folder, 'fig.png')
    #plt.savefig(figure_name)
    #return max(pressure) - min(pressure)


def get_pressure_drop(start, stop, folder):
    folder = os.path.join(folder, 'RESULT')
    spp = Postprocessing()
    vtm = spp.pa.get_last_modified(folder)
    filter = spp.pa.pa.OpenDataFile(vtm)
    pnew = spp.pa.get_line_plot(filter, start, stop, cell=False)['P']
    pnew = pnew[~np.isnan(pnew)]
    return pnew[0]-pnew[-1]
    #plt.plot(pressure)
    #figure_name = os.path.join(folder, 'fig.png')
    #plt.savefig(figure_name)
    #return max(pressure) - min(pressure)


def get_outlet_massflow_rate(folder, A_2d, A_3d, phases):

    spp = Postprocessing()
    folder = os.path.join(folder, 'RESULT')
    vtm = spp.pa.get_last_modified(folder)
    filter = spp.pa.pa.OpenDataFile(vtm)

    slice = spp.pa.get_custom_slice_3D(filter, 1.75, 0, 0, 1, 0, 0)

    results = {}
    for phase in phases:
        weight = ['U', str(phase.get_density()), 'HembI']
        var = "PhaseAlpha"+phase.get_index()
        mfr = spp.pa.massflow_avg(slice, weight, var, cell=False)
        mfr = mfr['massflow'][0]
        mf = mfr/A_2d
        results[phase.get_name()] = mf*A_3d
    return results
