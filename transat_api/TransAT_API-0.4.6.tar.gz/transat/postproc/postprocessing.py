import os
import numpy as np
import sys
import matplotlib.pyplot as plt
"""
.. module:: Postprocessing
   :platform: Unix, Windows
   :synopsis: Postprocessing module for TransAT output

.. moduleauthor:: Ascomp GmbH


"""


class Postprocessing(object):
    def __init__(self, sim = None):
        self.sim = sim
        try:
            import para_reader as pa
            self.pa = pa
        except ImportError:
            print "Error: Paraview python package is not installed"
            #sys.exit()

    def _adapt_points(self, spp, filter, point):
        bounds = spp.pa.get_bounds(filter)
        for i in range(3):
            p = point[i]
            if p > bounds[2*i+1]:
                p = bounds[2*i+1]
            if p < bounds[2*i]:
                p = bounds[2*1]
            point[i] = p
        return point


    def get_pressure_drop(self,folder,  start, stop):
        folder = os.path.join(folder, 'RESULT')
        spp = Postprocessing()
        pressure = {}
        for vtm in spp.pa.get_all(folder):
            time = spp.pa.get_time(vtm)
            if time is not None:
               time = float(time)
               para_reader = spp.pa.para_reader(vtm)
               start = self._adapt_points(spp, para_reader.threshold, start)
               stop = self._adapt_points(spp, para_reader.threshold, stop)
               with spp.pa.quiet():
                 pnew = spp.pa.get_line_plot(para_reader.threshold, start, stop, cell=False)['P']
               pnew = pnew[~np.isnan(pnew)]
               pressure[time] =pnew[0]-pnew[-1]
        return pressure

    def get_massflow_rate_2D(self, folder, A_2d, A_3d, phases, point, normal):
        folder = os.path.join(folder, 'RESULT')
        spp = Postprocessing()
        mfrs = {}
        for vtm in spp.pa.get_all(folder):
            time = spp.pa.get_time(vtm)
            try:
                para_reader = spp.pa.para_reader(vtm)
                point = self._adapt_points(spp, para_reader.threshold, point)
                slice = spp.pa.get_custom_slice_3D(para_reader.threshold, point[0], point[1], point[2], normal[0], normal[1], normal[2])

                results = {}
                for phase in phases:
                    weight = ['U', str(phase.get_density()), 'HembI']
                    var = "PhaseAlpha"+phase.get_index()
                    mfr = spp.pa.massflow_avg(slice, weight, var, cell=False)
                    mfr = mfr['massflow'][0]
                    mf = mfr/A_2d
                    results[phase.get_name()] = mf*A_3d
                mfrs[time] = results
            except:
                print "Could not get the mass flow rate at point "+str(point)
        return mfrs

    def plot(self, folder, name, x, y, xlabel, ylabel):
        figure_name = os.path.join(folder, name)

        try:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.scatter(x, y)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.savefig(figure_name)
            print "Figure saved in "+str(figure_name)
        except:
            print "could not plot with matplotlib"

    def get_bc_results(self, bc_name):
        tree = self.sim.setup.bcs.get_surface_tree()
        surfaces = tree.get_surfaces_by_bc_name(bc_name).surfaces

        var = "U"
        vtm  = self.sim.postprocess.pa.get_last_modified(os.path.join(self.sim.load_path(), "RESULT"))
        res = []
        for s in surfaces:
            res_sub = []
            for sub_s in s.subbcs:
                normal = sub_s.get_normal()
                corners = sub_s.get_corners()
                data = self.sim.postprocess.pa.pa.OpenDataFile(vtm)
                plane = self.sim.postprocess.pa.get_plane(data, corners, normal)
                avg = self.sim.postprocess.pa.massflow_avg(plane, weight=['HembI'], var=var, cell=False)
                res_sub.append(avg)


            normal = s.get_normal()
            corners = s.get_corners()
            data = self.sim.postprocess.pa.pa.OpenDataFile(vtm)
            plane = self.sim.postprocess.pa.get_plane(data, corners, normal)
            avg = self.sim.postprocess.pa.massflow_avg(plane, weight=['HembI'], var=var, cell=False)
            for key in avg.keys():
                for d in res_sub:
                    avg[key] -= d[key]
            res.append(avg)

        return res

