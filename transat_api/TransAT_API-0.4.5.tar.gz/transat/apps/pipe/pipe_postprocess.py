from transat.postproc.postprocessing import Postprocessing
import os
import numpy as np
import matplotlib.pyplot as plt

def plot_pressure(folder, points, name='fig.png'):

    figure_name = os.path.join(folder, name)
    folder = os.path.join(folder, 'RESULT')
    spp = Postprocessing()
    vtm = spp.pa.get_last_modified(folder)
    data = spp.pa.pa.OpenDataFile(vtm)

    pressure = np.array([])
    arc = np.array([])
    for i in range(len(points) - 1):
        p = spp.pa.get_line_plot(data, points[i], points[i + 1], cell=False)['P']
        a = spp.pa.get_line_plot(data, points[i], points[i + 1], cell=False)['arc_length']
        p = p[~np.isnan(p)]
        a = a[~np.isnan(p)]
        pressure = np.concatenate((pressure, p))
        arc = np.concatenate((arc, a))

    try:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(arc, pressure)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('P [Pa]')
        plt.savefig(figure_name)
        print "Figure saved in "+str(figure_name)
    except:
        print "could not plot with matplotlib"
        print "the pressure profile is "
        print str(pressure)

    return max(pressure) - min(pressure)


