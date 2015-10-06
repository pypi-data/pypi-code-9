"""
.. module:: sim_process
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: Petr Zikan <zikan.p@gmail.com>

This module contains just class SimProcess and logging setting.

"""
from __future__ import absolute_import
import logging
from probe.plotting.plotting import Plotting
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import constants as C
import statsmodels.api as sm
from .sim_common import SimCommon
import boltons.iterutils

from bokeh.io import vplot, output_notebook
from bokeh.io import show as bshow
from bokeh.plotting import figure as bfigure
from bokeh.models import LinearAxis, Range1d, Axis

cfg = {'debug': 2}


class MultiLineFormatter(logging.Formatter):
    """
    Hopefully, soon will be moved to its own class in another
    module
    """

    def __init__(self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        # hack: http://stackoverflow.com/a/5879524/533618
        backup_exc_text = record.exc_text
        record.exc_text = None
        formatted = logging.Formatter.format(self, record)
        header = formatted.split(record.message)[0]
        record.exc_test = backup_exc_text
        return header + ('\n' + header).join(it for it in record.message.split('\n') if it)


logger = logging.getLogger()
logger.setLevel({1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}.get(cfg['debug'], 0))
sh = logging.StreamHandler(sys.stderr)
fmt = '%(asctime)s.%(msecs).03d %(process)+5s %(levelname)-8s %(filename)s:%(lineno)d:%(funcName)s(): %(message)s'
sh.setFormatter(MultiLineFormatter(fmt, '%Y-%m-%d %H:%M:%S'))
logger.handlers = []
logger.addHandler(sh)


class SimProcess(SimCommon):
    """
    This is a description of a class SimProcess. It serves for a "first-level"
    manipulation with hdf5 data from simulation.

    After initialization with hdf5 file, every object holds all important information
    about the simulation. As attributes it stores following data

    * self.m_e - mass of electron
    * self.m_Ar - mass of argon ion
    * self.commons - dict {group_number: group_name}
    * self.runs - dict {run_number: group_name}
    * self.gstats - dcit {gstats_number: group_name}
    * self.inits - same for inits groups
    * self.saves - same for saves groups
    * self.sweeps - same for sweeps groups
    * self.data - time evolution of simulation - groups ts_*
    * self.no_runs - number of runs
    * self.no_outputs - number of time evolution outputs
    * self.r_grid - dict {run_number: r_grid}
    * self.rm_grid - dict {run_number: rm_grid}
    * self.vol_grid - dict {run_number: vol_grid}
    * self.params - dict {run_number: params}, where params is dict of attrs stored in common group for a given run_number
    * self.outputs - list of all output numbers - i.e. numbers of all ts_* groups
    * self.stats - dict of lists:
        * 'current' : current in ts_*
        * 'nprobe_el' : number of electron to probe
        * 'nnew_el' : new electrons
        * 'nprobe_ari' : argon ions to probe
        * 'nsheath_el' : number of electrons that left domain thru boundary
        * 'nsheath_ari' : same for argon ion
        * 'nnew_ari' : new argon ion
        * 'nactive_el' : number of electrons in the domain
        * 'nactive_ari' : as for ions
        * 'time' : TODO
        * 'itime' : timesteps of outputs
        * 'elapsed_time' : time in second between outputs
    """

    def __init__(self, h5_filename):
        """
        Constructor.

        Args:
            h5_filename (str): path to hdf5 file
        """
        SimCommon.__init__(self, h5_filename)

        self.m_e = C.m_e
        self.m_Ar = C.m_u * 39.948 - self.m_e

        self.commons = self.get_list_of_groups_as_dict('common')
        logger.debug('self.commons: %s', self.commons)

        self.runs = [int(x.split('_')[1]) for x in self.commons.values()]
        logger.debug('self.runs: %s', self.runs)

        self.gstats = self.get_list_of_groups_as_dict('gstats')
#        logger.debug('self.gstats: %s', self.gstats)

        self.inits = self.get_list_of_groups_as_dict('init')
#        logger.debug('self.inits: %s', self.inits)

        self.saves = self.get_list_of_groups_as_dict('save')
#        logger.debug('self.saves: %s', self.saves)

        self.sweeps = self.get_list_of_groups_as_dict('sweep')
#        logger.debug('self.sweeps: %s', self.sweeps)

        self.data = self.get_list_of_groups_as_dict('ts')
#        logger.debug('self.data: %s', self.data)

        assert len(self.commons) == len(self.inits)

        self.no_runs = len(self.commons)
        logger.info('self.no_runs: %s', self.no_runs)

        self.no_outputs = len(self.data)
        logger.info('self.no_outputs: %s', self.no_outputs)

        self.r_grid = dict()
        self.rm_grid = dict()
        self.vol_grid = dict()
        self.params = dict()
        self.outputs = dict()

        for no_run in self.runs:
            self.r_grid[no_run] = self.h5_f['{}/r_grid'.format(self.commons[no_run])][...]
            self.rm_grid[no_run] = self.h5_f['{}/rm_grid'.format(self.commons[no_run])][...]
            self.vol_grid[no_run] = self.h5_f['{}/vol_grid'.format(self.commons[no_run])][...]
            self.params[no_run] = self.get_attrs_as_dict(self.commons[no_run])

        outputs = [1]
        last_output = 0
        for no_run in self.runs:
            Ntimes = self.params[no_run]['Ntimes']
            out_every = self.params[no_run]['out_every']
            for output_no in xrange(out_every + last_output, Ntimes + last_output + 1, out_every):
                outputs.append(output_no)
                last_output = output_no
            self.outputs[no_run] = outputs
            outputs = []

        logger.debug('self.r_grid: %s', self.r_grid)
        logger.debug('self.rm_grid: %s', self.rm_grid)
        logger.debug('self.vol_grid: %s', self.vol_grid)

        logger.debug('----------------')
        logger.debug('self.params[0]:')
        for param in self.params[0]:
            if isinstance(self.params[0][param], int) or isinstance(self.params[0][param], float):
                logger.debug('%s: %5.4e', param, self.params[0][param])
            else:
                logger.debug('%s: %s', param, self.params[0][param])

        self.stats = {
            'current' : list(),
            'nprobe_el' : list(),
            'nnew_el' : list(),
            'nprobe_ari' : list(),
            'nsheath_el' : list(),
            'nsheath_ari' : list(),
            'nnew_ari' : list(),
            'nactive_el' : list(),
            'nactive_ari' : list(),
            'time' : list(),
            'itime' : list(),
            'elapsed_time' : list()
        }

        self.get_stats()

        logger.debug('----------------')
        logger.debug('self.stats:')
        for stat in self.stats:
            logger.debug('%s: %s', stat, self.stats[stat])


    def __del__(self):
        self.h5_f.close()


    def last_output(self):
        return sorted(self.data.keys())[-1]


    def close(self):
        """
        Close opend hdf5 file refferenced by self.h5_f

        """
        self.h5_f.close()

    def stats_linear_model(self, variable, ts_from=1, ts_to=-1):
        """
        Fit linear model 'y = k * x + q', where y is
        self.stats[variable] and x is self.stats['itime']

        It prints model statistics and shows fit in a plot.

        Args:
            variable (str) - name of variable to fit

        Kwargs:
            ts_from (int) - number of timestep (from beginning by default)
            ts_to (int) - number of timestep (all by default)
        """
        index_from = self.timestep2itimeindex(ts_from)
        index_to = self.timestep2itimeindex(ts_to)

        x = self.stats['itime'][index_from:index_to+1]
        y = self.stats[variable][index_from:index_to+1]

        x_all = self.stats['itime']
        y_all = self.stats[variable]

        df = pd.DataFrame({'k': x, 'y': y})
        df['q'] = np.ones(len(df))
        model = sm.OLS(df['y'], df[['k', 'q']]).fit()
        print model.summary()

        fig, ax = plt.subplots(1, 1)
        ax.plot(x_all, y_all)

        model_x = np.linspace(x[0], x[-1], 1000)
        model_y = model.params['k'] * model_x + model.params['q']
        ax.plot(model_x, model_y)
        plt.show()


    def stats_constant_model(self, variable, ts_from=1, ts_to=-1,
                             model_points=1000):
        """
        Fit linear model 'y = q', where y is
        self.stats[variable] a q is constant.

        It prints model statistics and shows fit in a plot.

        Args:
            variable (str) - name of variable to fit

        Kwargs:
            ts_from (int) - number of timestep (from beginning by default)
            ts_to (int) - number of timestep (all by default)
        """
        index_from = self.timestep2itimeindex(ts_from)
        index_to = self.timestep2itimeindex(ts_to)

        x = self.stats['itime'][index_from:index_to+1]
        y = self.stats[variable][index_from:index_to+1]

        df = pd.DataFrame({'y': y})
        df['q'] = np.ones(len(df))
        model = sm.OLS(df['y'], df[['q']]).fit()

        x_all = self.stats['itime']
        y_all = self.stats[variable]

        model_x = np.linspace(x[0], x[-1], model_points)
        model_y = np.zeros(model_points) + model.params['q']

        return model, x_all, y_all, model_x, model_y



    def plot_stats_constant_model(self, variable, ts_from=1, ts_to=-1,
                                  model_points=1000, linewidth=2.0):

        fit_result = self.stats_constant_model(variable, ts_from=ts_from,
                                               ts_to=ts_to,
                                               model_points=model_points)

        model, x_all, y_all, model_x, model_y = fit_result
        print model.summary()
        print 'q = {}'.format(model.params[0])

        fig, ax = plt.subplots(1, 1)
        ax.plot(x_all, y_all)
        ax.plot(model_x, model_y, linewidth=linewidth)
        plt.show()

    def get_stats(self):
        """
        Returns statistics about time evolution of macroscopic parameters.

        Returns:
            dict - {attr_name: list of values (corresponds to list of values
                               of time evolution of attr_name parsed from all
                               ts_* groups)}
        """
        for ts in sorted(self.data.keys()):
            for attr, value in self.h5_f['/{}'.format(self.data[ts])].attrs.iteritems():
                self.stats[attr].append(value[0])

    def animate_profiles(self, ne_ylim=None, phi_ylim=None, ts_from=1, n0=None):
        """
        Pops up an "animation" of particles' densities evolution.

        """
        fig, ax = plt.subplots(2, 1, sharex=True)

        tss = sorted(self.data.keys())
        ts_from = tss.index(ts_from)

        for itime in tss[ts_from:]:
            print itime

            ax[0].clear()
            ax[1].clear()

            if ne_ylim is not None:
                ax[0].set_ylim(ne_ylim)

            if phi_ylim is not None:
                ax[1].set_ylim(phi_ylim)

            ax[0].plot(self.r_grid[0], self.h5_f[self.data[itime]]['num_el_grid'][...] / self.vol_grid[0], 'r-')
            ax[0].plot(self.r_grid[0], self.h5_f[self.data[itime]]['num_ari_grid'][...] / self.vol_grid[0], 'g-')
            if n0:
                ax[0].plot((self.r_grid[0][0], self.r_grid[0][-1]), (n0, n0))
            ax[1].plot(self.r_grid[0], self.h5_f[self.data[itime]]['phi_grid'][...])
            plt.draw()
            plt.pause(0.1)

    def profiles_constant_model(self, variable, ts_from=1, ts_to=-1,
                                model_points=1000, fit_from=None, fit_to=None):

        index_from = self.timestep2itimeindex(ts_from)
        index_to = self.timestep2itimeindex(ts_to)

        if fit_from is None:
            fit_from = self.params[0]['r_p']

        if fit_to is None:
            fit_to = self.params[0]['r_d']

        averaged_profiles = self.average_profiles(index_from, index_to)
        profile = averaged_profiles[variable]

        good_indexes = np.logical_and(self.r_grid[0] >= fit_from, self.r_grid[0] <= fit_to)

        x = self.r_grid[0][good_indexes]
        y = profile[good_indexes]

        df = pd.DataFrame({'y': y})
        df['q'] = np.ones(len(df))
        df.dropna(inplace=True)
        model = sm.OLS(df['y'], df[['q']]).fit()

        x_all = self.r_grid[0]
        y_all = profile

        model_x = np.linspace(x[0], x[-1], model_points)
        model_y = np.zeros(model_points) + model.params['q']

        return model, x_all, y_all, model_x, model_y

    def plot_profiles_constant_model(self, variable, ts_from=1, ts_to=-1,
                                     model_points=1000, linewidth=2.0,
                                     fit_from=None, fit_to=None):

        fit_result = self.profiles_constant_model(variable, ts_from=ts_from,
                                                  ts_to=ts_to,
                                                  model_points=model_points,
                                                  fit_from=fit_from, fit_to=fit_to)

        model, x_all, y_all, model_x, model_y = fit_result
        print model.summary()
        print 'q = {}'.format(model.params[0])

        fig, ax = plt.subplots(1, 1)
        ax.plot(x_all, y_all)
        ax.plot(model_x, model_y, linewidth=linewidth)
        plt.show()

    def plot_ts(self, ts):
        """
        Pops up a plot with time step snapshot - subplot with (densities, fields,
        temperatures and radial velocities).

        Args:
            ts (int) - timestep (corresponds to '???' of ts_???? groups)

        """
        fig, ax = plt.subplots(2, 3)

        r = self.r_grid[0]
        ne = self.h5_f['/{}/num_el_grid'.format(self.data[ts])] / self.vol_grid[0]
        ni = self.h5_f['/{}/num_ari_grid'.format(self.data[ts])] / self.vol_grid[0]

        ax[0, 0].plot(r, ne, 'r-', label='n_e')
        ax[0, 0].plot(r, ni, 'g-', label='n_i')
        ax[0, 0].set_xlabel('r [m]')
        ax[0, 0].set_ylabel('n_e, n_i [m^-3]')
        ax[0, 0].legend(loc='best')

        phi = self.h5_f['/{}/phi_grid'.format(self.data[ts])]

        ax[1, 0].plot(r, phi, 'b-')
        ax[1, 0].set_xlabel('r [m]')
        ax[1, 0].set_ylabel('phi [V]')

        er = self.h5_f['/{}/er_grid'.format(self.data[ts])]

        ax10_2 = ax[1, 0].twinx()
        ax10_2.plot(r, er, 'r-')
        ax10_2.set_ylabel('Er [V/m]')

        vre = self.h5_f['/{}/lstat_el_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...]

        ax[0, 1].plot(r, vre, 'r-')
        ax[0, 1].set_xlabel('r [m]')
        ax[0, 1].set_ylabel('vr [m/s]')
        ax[0, 1].set_title('electron')

        Te = self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...] / (3 * C.k)

        ax[1, 1].plot(r, Te, 'r-')
        ax[1, 1].set_xlabel('r [m]')
        ax[1, 1].set_ylabel('T [K]')
        ax[1, 1].set_title('electron')

        vri = self.h5_f['/{}/lstat_ari_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...]
        ax[0, 2].plot(r, vri, 'g-')
        ax[0, 2].set_xlabel('r [m]')
        ax[0, 2].set_ylabel('vr [m/s]')
        ax[0, 2].set_title('ion')

        Ti = self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...] / (3 * C.k)
        ax[1, 2].plot(r, Ti, 'g-')
        ax[1, 2].set_xlabel('r [m]')
        ax[1, 2].set_ylabel('T [K]')
        ax[1, 2].set_title('ion')

        plt.show()

    def blot_ts(self, ts):
        """
        r = sp.r_gri	ts=sp.last_output()d[0]
        Pops up an interactive plot with time step snapshot - subplot with (densities, fields,
            temperatures and radial velocities).

            Args:
                ts (int) - timestep (corresponds to '???' of ts_???? groups)

            """
        r = self.r_grid[0]
        ne = self.h5_f['/{}/num_el_grid'.format(self.data[ts])] / self.vol_grid[0]
        ni = self.h5_f['/{}/num_ari_grid'.format(self.data[ts])] / self.vol_grid[0]
        s1 = bfigure(width=850, plot_height=400, title = None, x_axis_label="r [m]", y_axis_label="n_e, n_i [m^-3]")
        s1.y_range = Range1d(start=ne[np.nanargmin(ne[1:-1])+1]*0.97,end=ne[np.nanargmax(ne[1:-1])+1]*1.03)
        s1.line(r, ne[1:-1], line_width=1, color="red")
        s1.line(r, ni[1:-1], line_width=1, color="green")

        phi = self.h5_f['/{}/phi_grid'.format(self.data[ts])]
        er = self.h5_f['/{}/er_grid'.format(self.data[ts])]
        s2 = bfigure(width=850, plot_height=400, title = None, x_axis_label="r [m]", y_axis_label="phi [V]")
        s2.y_range = Range1d(start=phi[np.nanargmin(phi[1:-1])+1]*0.97,end=phi[np.nanargmax(phi[1:-1])+1]*1.03)
        s2.line(r, phi[1:-1], line_width=1, color="red")
        s2.extra_y_ranges = {"Er": Range1d(start=er[np.nanargmin(er[1:-1])+1]*0.97,end=er[np.nanargmax(er[1:-1])+1]*1.03)}
        s2.line(r, er[1:-1], line_width=1, color="blue", y_range_name="Er")
        s2.add_layout(LinearAxis(y_range_name="Er",axis_label="Er [V/m]"), 'right')

        vre = self.h5_f['/{}/lstat_el_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...]
        s3 = bfigure(width=850, plot_height=400, title = "electron", x_axis_label="r [m]", y_axis_label="vr [m/s]")
        s3.y_range = Range1d(start=vre[np.nanargmin(vre[1:-1])+1]*0.97,end=vre[np.nanargmax(vre[1:-1])+1]*1.03)
        s3.line(r, vre[1:-1], line_width=1, color="red")

        Te = self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...] / (3 * C.k)
        s4 = bfigure(width=850, plot_height=400, title = "electron", x_axis_label="r [m]", y_axis_label="T [K]")
        s4.y_range = Range1d(start=Te[np.nanargmin(Te[1:-1])+1]*0.97,end=Te[np.nanargmax(Te[1:-1])+1]*1.03)
        s4.line(r, Te, line_width=1, color="red")

        vri = self.h5_f['/{}/lstat_ari_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...]
        s5 = bfigure(width=850, plot_height=400, title = "ion", x_axis_label="r [m]", y_axis_label="vr [m/s]")
        s5.y_range = Range1d(start=vri[np.nanargmin(vri[1:-1])+1]*0.97,end=vri[np.nanargmax(vri[1:-1])+1]*1.03)
        s5.line(r, vri[1:-1], line_width=1, color="green")

        Ti = self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...] / (3 * C.k)
        s6 = bfigure(width=850, plot_height=400, title = "ion", x_axis_label="r [m]", y_axis_label="T [K]")
        s6.y_range = Range1d(start=Ti[np.nanargmin(Ti[1:-1])+1]*0.97,end=Ti[np.nanargmax(Ti[1:-1])+1]*1.03)
        s6.line(r, Ti, line_width=1, color="green")

        p = vplot(s1, s2, s3, s4, s5, s6)

        bshow(p)

    def plot_profiles(self, list_of_ts):
        """
        Pops up a plot with comparison of particles' densities at various
        timesteps.

        Args:
            list_of_ts (list) - timesteps

        """
        if not isinstance(list_of_ts, list):
            list_of_ts = [list_of_ts]

        list_to_plot = []
        list_of_labels = []

        for ts in list_of_ts:
            list_to_plot.append(self.h5_f['/{}/num_el_grid'.format(self.data[ts])][...] / self.vol_grid[0])
            list_of_labels.append('{} ne'.format(ts))
            list_to_plot.append(self.h5_f['/{}/num_ari_grid'.format(self.data[ts])][...] / self.vol_grid[0])
            list_of_labels.append('{} ni'.format(ts))

        Plotting.plot_single_ax([self.r_grid[0]] * len(list_to_plot), list_to_plot, list_of_labels=list_of_labels,
                                xlabel='r [m]', ylabel='n_e, n_i [m^-3]')
#                                print_to_file=print_to_file, print_filename=print_filename)


    @staticmethod
    def fill_subplot_twinx(this_ax, this_ax2, x, y, x_label='x', y_label=('y1', 'y2'),
                           style=('b-', 'r-'), line_desc=('l1','l2')):

        lns1 = this_ax.plot(x, y[0], style[0], label=line_desc[0])
        this_ax.set_xlabel(x_label)
        this_ax.set_ylabel(y_label[0])
        lns2 = this_ax2.plot(x, y[1], style[1], label=line_desc[1])
        this_ax2.set_ylabel(y_label[1])
        lns = lns1+lns2
        labs = [l.get_label() for l in lns]

        return lns, labs

    @staticmethod
    def fill_subplot(ax, x, y, x_label='x', y_label='y',
                     style='b-', line_desc='l1', linewidth=1.0):

        ax.plot(x, y, style, label=line_desc, linewidth=linewidth)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend(loc='best')

    def plot_stats(self):
        """
        Pops up a subplot with time evolution of macrosopic parameters:
            * number of particles in domain
            * number incident particles to the probe
            * number of particles that left domain thru outer boundary
            * current
            * ...
        """

        fig, ax = plt.subplots(3, 2)
        fig.subplots_adjust(left=0.05, wspace=0.45)

        this_ax = ax[0, 0]; ax2 = this_ax.twinx()
        self.fill_subplot_twinx(this_ax, ax2, self.stats['itime'], (self.stats['nprobe_el'], self.stats['nprobe_ari']),
                                x_label = '# output', y_label=('probe el', 'probe ion'),
                                style=('r-', 'g-'), line_desc=('el', 'ion'))

        this_ax = ax[1, 0]; ax2 = this_ax.twinx()
        self.fill_subplot_twinx(this_ax, ax2, self.stats['itime'], (self.stats['nnew_el'], self.stats['nnew_ari']),
                                x_label = '# output', y_label=('new el', 'new ion'),
                                style=('r-', 'g-'), line_desc=('el', 'ion'))

        this_ax = ax[2, 0]; ax2 = this_ax.twinx()
        self.fill_subplot_twinx(this_ax, ax2, self.stats['itime'], (self.stats['nsheath_el'], self.stats['nsheath_ari']),
                                x_label = '# output', y_label=('sheath el', 'sheath ion'),
                                style=('r-', 'g-'), line_desc=('el', 'ion'))

        self.fill_subplot(ax[0, 1], self.stats['itime'], self.stats['current'],
                          x_label = '# output', y_label='current',
                          style='b-', line_desc='current')

        this_ax = ax[1, 1]; ax2 = this_ax.twinx()
        self.fill_subplot_twinx(this_ax, ax2, self.stats['itime'], (self.stats['nactive_el'], self.stats['nactive_ari']),
                                x_label = '# output', y_label=('active el', 'active ion'),
                                style=('r-', 'g-'), line_desc=('el', 'ion'))

        self.fill_subplot(ax[2, 1], self.stats['itime'], self.stats['elapsed_time'],
                          x_label = '# output', y_label='elapsed time [s]',
                          style='b-', line_desc='time')

        plt.show()

    def blot_stats(self):
        """
        Pops up an interactive subplot with time evolution of macrosopic parameters:
            * number of particles in domain
            * number incident particles to the probe
            * number of particles that left domain thru outer boundary
            * current
            * ...
        """

        s1 = bfigure(width=850, plot_height=400, title = None, x_axis_label="output", y_axis_label="nprobe_el")
        s1.y_range = Range1d(start=min(self.stats["nprobe_el"][1:-1])*0.97,end=max(self.stats["nprobe_el"][1:-1])*1.03)
        s1.line(self.stats["itime"], self.stats["nprobe_el"][1:-1], line_width=1, color="red")
        s1.extra_y_ranges = {"ion": Range1d(start=(min(self.stats["nprobe_ari"][1:-1])-0.1)*0.97,end=(max(self.stats["nprobe_ari"][1:-1])+0.1)*1.03)}
        s1.line(self.stats["itime"], self.stats["nprobe_ari"][1:-1], line_width=1, color="green", y_range_name="ion")
        s1.add_layout(LinearAxis(y_range_name="ion",axis_label="nprobe_ari"), 'right')

        s2 = bfigure(width=850, plot_height=400, title = None, x_axis_label="output", y_axis_label="nnew_el")
        s2.y_range = Range1d(start=min(self.stats["nnew_el"][1:-1])*0.97,end=max(self.stats["nnew_el"][1:-1])*1.03)
        s2.line(self.stats["itime"], self.stats["nnew_el"][1:-1], line_width=1, color="red")
        s2.extra_y_ranges = {"ion": Range1d(start=min(self.stats["nnew_ari"][1:-1])*0.97,end=max(self.stats["nnew_ari"][1:-1])*1.03)}
        s2.line(self.stats["itime"], self.stats["nnew_ari"][1:-1], line_width=1, color="green", y_range_name="ion")
        s2.add_layout(LinearAxis(y_range_name="ion",axis_label="nnew_ari"), 'right')

        s3 = bfigure(width=850, plot_height=400, title = None, x_axis_label="output", y_axis_label="nsheath_el")
        s3.y_range = Range1d(start=min(self.stats["nsheath_el"][1:-1])*0.97,end=max(self.stats["nsheath_el"][1:-1])*1.03)
        s3.line(self.stats["itime"], self.stats["nsheath_el"][1:-1], line_width=1, color="red")
        s3.extra_y_ranges = {"ion": Range1d(start=min(self.stats["nsheath_ari"][1:-1])*0.97,end=max(self.stats["nsheath_ari"][1:-1])*1.03)}
        s3.line(self.stats["itime"], self.stats["nsheath_ari"][1:-1], line_width=1, color="green", y_range_name="ion")
        s3.add_layout(LinearAxis(y_range_name="ion",axis_label="nsheath_ari"), 'right')

        s4 = bfigure(width=850, plot_height=400, title = None, x_axis_label="output", y_axis_label="nactive_el")
        s4.y_range = Range1d(start=min(self.stats["nactive_el"][1:-1])*0.97,end=max(self.stats["nactive_el"][1:-1])*1.03)
        s4.line(self.stats["itime"], self.stats["nactive_el"][1:-1], line_width=1, color="red")
        s4.extra_y_ranges = {"ion": Range1d(start=min(self.stats["nactive_ari"][1:-1])*0.97,end=max(self.stats["nactive_ari"][1:-1])*1.03)}
        s4.line(self.stats["itime"], self.stats["nactive_ari"][1:-1], line_width=1, color="green", y_range_name="ion")
        s4.add_layout(LinearAxis(y_range_name="ion",axis_label="nactive_ari"), 'right')

        s5 = bfigure(width=850, plot_height=400, title = None, x_axis_label="output", y_axis_label="current")
        s5.line(self.stats["itime"], self.stats["current"][1:-1], line_width=1, color="blue")

        s6 = bfigure(width=850, plot_height=400, title = None, x_axis_label="output", y_axis_label="elapsed_time")
        s6.line(self.stats["itime"], self.stats["elapsed_time"][1:-1], line_width=1, color="blue")

        p = vplot(s1, s2, s3, s4, s5, s6)

        bshow(p)


    def timestep2itimeindex(self, timestep_number):
        """
        Converts timestep number to corresponding index for
        self.data indexing. Therefore, this number has to
        correspond to a timestep number when output was printed.

        Args:
            timestep_number (int) - timestep number

        Returns:
            index (int) - index in self.data
        """

        tss = self.stats['itime']

        if timestep_number == -1:
            index = tss[-1]
            return index

        try:
            index = tss.index(timestep_number)
        except ValueError:
            logger.error('there is no timestep %s', timestep_number)
            return None

        return index

    def timestep2dataindex(self, timestep_number):
        """
        Converts timestep number to corresponding index for
        self.data indexing. Therefore, this number has to
        correspond to a timestep number when output was printed.

        Args:
            timestep_number (int) - timestep number

        Returns:
            index (int) - index in self.data
        """

        tss = sorted(self.data.keys())

        if timestep_number == -1:
            index = tss[-1]
            return index

        try:
            index = tss.index(timestep_number)
        except ValueError:
            logger.error('there is no timestep %s', timestep_number)
            return None

        return index

    def average_profiles(self, index_from, index_to):
        """
        Computes average of variables of interest over specified time interval.

        Args:
            index_from (int) - position in self.data to average from
            index_to (int) - position in self.data to average to

        Returns:
            dict - {variable_name: averaged numpy array of the variable}

            variables:
                * ne
                * ni
                * phi
                * er
                * Te
                * vre
                * Ti
                * vri
        """

        tss = sorted(self.data.keys())

        phi = self.h5_f['/{}/phi_grid'.format(self.data[tss[index_from]])][...]
        er = self.h5_f['/{}/er_grid'.format(self.data[tss[index_from]])][...]

        ne = self.h5_f['/{}/num_el_grid'.format(self.data[tss[index_from]])][...]
        ni = self.h5_f['/{}/num_ari_grid'.format(self.data[tss[index_from]])][...]

        Te = self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[tss[index_from]])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[tss[index_from]])][...] / (3 * C.k)
        vre = self.h5_f['/{}/lstat_el_vr'.format(self.data[tss[index_from]])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[tss[index_from]])][...]

        Ti = self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[tss[index_from]])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[tss[index_from]])][...] / (3 * C.k)
        vri = self.h5_f['/{}/lstat_ari_vr'.format(self.data[tss[index_from]])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[tss[index_from]])][...]


        for ts in tss[index_from+1:index_to+1]:
            ne += self.h5_f['/{}/num_el_grid'.format(self.data[ts])][...]
            ni += self.h5_f['/{}/num_ari_grid'.format(self.data[ts])][...]

            phi += self.h5_f['/{}/phi_grid'.format(self.data[ts])][...]
            er += self.h5_f['/{}/er_grid'.format(self.data[ts])][...]

            Te += self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...] / (3 * C.k)
            vre += self.h5_f['/{}/lstat_el_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...]

            Ti += self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...] / (3 * C.k)
            vri += self.h5_f['/{}/lstat_ari_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...]

        ne /= len(tss[index_from:index_to+1])
        ni /= len(tss[index_from:index_to+1])
        ne /= self.vol_grid[0]
        ni /= self.vol_grid[0]

        phi /= len(tss[index_from:index_to+1])
        er /= len(tss[index_from:index_to+1])

        Te /= len(tss[index_from:index_to+1])
        vre /= len(tss[index_from:index_to+1])

        Ti /= len(tss[index_from:index_to+1])
        vri /= len(tss[index_from:index_to+1])

        ne_stddev = (ne -
                     self.h5_f['/{}/num_el_grid'.format(self.data[tss[index_from]])][...]
                    / self.vol_grid[0])**2
        ni_stddev = (ni -
                     self.h5_f['/{}/num_ari_grid'.format(self.data[tss[index_from]])][...]
                    / self.vol_grid[0])**2

        phi_stddev = (phi -
                      self.h5_f['/{}/phi_grid'.format(self.data[tss[index_from]])][...])**2
        er_stddev = (er -
                     self.h5_f['/{}/er_grid'.format(self.data[tss[index_from]])][...])**2

        Te_stddev = (Te - self.m_e *
                     self.h5_f['/{}/lstat_el_v2'.format(self.data[tss[index_from]])][...]
                     /
                     self.h5_f['/{}/lstat_el_num'.format(self.data[tss[index_from]])][...]
                     / (3 * C.k))**2
        vre_stddev = (vre -
                      self.h5_f['/{}/lstat_el_vr'.format(self.data[tss[index_from]])][...]
                      /
                      self.h5_f['/{}/lstat_el_num'.format(self.data[tss[index_from]])][...])**2

        Ti_stddev = (Ti - self.m_Ar *
                     self.h5_f['/{}/lstat_ari_v2'.format(self.data[tss[index_from]])][...]
                     /
                     self.h5_f['/{}/lstat_ari_num'.format(self.data[tss[index_from]])][...]
                     / (3 * C.k))**2
        vri_stddev = (vri -
                      self.h5_f['/{}/lstat_ari_vr'.format(self.data[tss[index_from]])][...]
                      /
                      self.h5_f['/{}/lstat_ari_num'.format(self.data[tss[index_from]])][...])**2

        for ts in tss[index_from+1:index_to+1]:
            ne_stddev += (ne - self.h5_f['/{}/num_el_grid'.format(self.data[ts])][...] / self.vol_grid[0])**2
            ni_stddev += (ni - self.h5_f['/{}/num_ari_grid'.format(self.data[ts])][...] / self.vol_grid[0])**2
            phi_stddev += (phi - self.h5_f['/{}/phi_grid'.format(self.data[ts])][...])**2
            er_stddev += (er - self.h5_f['/{}/er_grid'.format(self.data[ts])][...])**2
            Te_stddev += (Te - self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...] / (3 * C.k))**2
            vre_stddev += (vre - self.h5_f['/{}/lstat_el_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...])**2
            Ti_stddev += (Ti - self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...] / (3 * C.k))**2
            vri_stddev += (vri - self.h5_f['/{}/lstat_ari_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...])**2

        ne_stddev /= len(tss[index_from:index_to+1])-1
        ni_stddev /= len(tss[index_from:index_to+1])-1
        phi_stddev /= len(tss[index_from:index_to+1])-1
        er_stddev /= len(tss[index_from:index_to+1])-1
        Te_stddev /= len(tss[index_from:index_to+1])-1
        vre_stddev /= len(tss[index_from:index_to+1])-1
        Ti_stddev /= len(tss[index_from:index_to+1])-1
        vri_stddev /= len(tss[index_from:index_to+1])-1

        ne_stddev = np.sqrt(ne_stddev)
        ni_stddev = np.sqrt(ni_stddev)
        phi_stddev = np.sqrt(phi_stddev)
        er_stddev = np.sqrt(er_stddev)
        Te_stddev = np.sqrt(Te_stddev)
        vre_stddev = np.sqrt(vre_stddev)
        Ti_stddev = np.sqrt(Ti_stddev)
        vri_stddev = np.sqrt(vri_stddev)

        ne_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        ni_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        phi_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        er_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        Te_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        vre_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        Ti_stddev /= np.sqrt(len(tss[index_from:index_to+1]))
        vri_stddev /= np.sqrt(len(tss[index_from:index_to+1]))






        #ne_stddev = np.std(self.h5_f['/{}/num_el_grid'.format(self.data[tss[index_from:index_to+1]])][...])
        #ni_stddev = np.std(self.h5_f['/{}/num_ari_grid'.format(self.data[tss[index_from:index_to+1]])][...])
        #
        #phi_stddev = np.std(self.h5_f['/{}/phi_grid'.format(self.data[tss[index_from:index_to+1]])][...])
        #er_stddev = np.std(self.h5_f['/{}/er_grid'.format(self.data[tss[index_from:index_to+1]])][...])
        #
        #Te_stddev = np.std(self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[tss[index_from:index_to+1]])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[tss[index_from:index_to+1]])][...] / (3 * C.k))
        #vre_stddev = np.std(self.h5_f['/{}/lstat_el_vr'.format(self.data[tss[index_from:index_to+1]])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[tss[index_from:index_to+1]])][...])
        #
        #Ti_stddev = np.std(self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[tss[index_from]])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...] / (3 * C.k))
        #vri_stddev = np.std(self.h5_f['/{}/lstat_ari_vr'.format(self.data[tss[index_from]])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...])

        return {
            'phi': phi,
            'er': er,
            'ne': ne,
            'ni': ni,
            'Te': Te,
            'vre': vre,
            'Ti': Ti,
            'vri': vri,
            'phi_stddev': phi_stddev,
            'er_stddev': er_stddev,
            'ne_stddev': ne_stddev,
            'ni_stddev': ni_stddev,
            'Te_stddev': Te_stddev,
            'vre_stddev': vre_stddev,
            'Ti_stddev': Ti_stddev,
            'vri_stddev': vri_stddev,
        }

    def plot_averaged_profiles(self, ts_from=1, ts_to=-1, plot_n0=True, labels=None,
                               markers=('-', '--'), linewidth=[1.0, 2.0],
                               only_densities=False, only_potential=False,
                               only_electrons=False, only_ions=False):
        """
        Pops up plot of averaged profiles over specified time interval.

        Args:
            ts_from (int) - number of timestep to average from
            ts_to (int) - number of timestep to average to
        """

        is_iterable = boltons.iterutils.is_iterable

        only_one_plot = False
        if only_densities or only_potential or only_electrons or only_ions:
            only_one_plot = True

        more_plots = False
        if is_iterable(ts_from):
            assert is_iterable(ts_to)
            assert len(ts_from) == len(ts_to)
            more_plots = True

        if not labels and more_plots:
            labels = [''] * len(ts_from)

        if is_iterable(ts_from):
            index_from = [self.timestep2dataindex(ts_f) for ts_f in ts_from]
        else:
            index_from = self.timestep2dataindex(ts_from)

        if is_iterable(ts_to):
            index_to = [self.timestep2dataindex(ts_t) for ts_t in ts_to]
        else:
            index_to = self.timestep2dataindex(ts_to)

        if more_plots:
            averaged_profiles = list()
            for index_f, index_t in zip(index_from, index_to):
                averaged_profiles.append(self.average_profiles(index_f, index_t))
        else:
            averaged_profiles = self.average_profiles(index_from, index_to)

        r = self.r_grid[0]
        if more_plots:
            ne = [averaged_profile['ne'] for averaged_profile in averaged_profiles]
            ni = [averaged_profile['ni'] for averaged_profile in averaged_profiles]
            phi = [averaged_profile['phi'] for averaged_profile in averaged_profiles]
            er = [averaged_profile['er'] for averaged_profile in averaged_profiles]
            Te = [averaged_profile['Te'] for averaged_profile in averaged_profiles]
            vre = [averaged_profile['vre'] for averaged_profile in averaged_profiles]
            Ti = [averaged_profile['Ti'] for averaged_profile in averaged_profiles]
            vri = [averaged_profile['vri'] for averaged_profile in averaged_profiles]
        else:
            ne = averaged_profiles['ne']
            ni = averaged_profiles['ni']
            phi = averaged_profiles['phi']
            er = averaged_profiles['er']
            Te = averaged_profiles['Te']
            vre = averaged_profiles['vre']
            Ti = averaged_profiles['Ti']
            vri = averaged_profiles['vri']

        if only_one_plot:
            fig, ax = plt.subplots(1, 1)
        else:
            fig, ax = plt.subplots(2, 2)
            fig.subplots_adjust(left=0.05, wspace=0.45)

        if only_densities:
            this_ax = ax
        elif only_potential or only_electrons or only_ions:
            this_ax = None
        else:
            this_ax = ax[0, 0]

        try:
            if plot_n0:
                this_ax.plot([self.params[0]['r_p'], self.params[0]['r_d']], [self.params[0]['n_e'], self.params[0]['n_e']], 'k--', label='n0')
            if more_plots:
                for var, marker, label, lw in zip(ne, markers[:len(ne)], labels, linewidth):
                    self.fill_subplot(this_ax, r, var, x_label='r [m]', y_label='ne, ni [m^-3]',
                                    style='r{}'.format(marker), line_desc='ne {}'.format(label),
                                    linewidth=lw)
            else:
                self.fill_subplot(this_ax, r, ne, x_label = 'r [m]', y_label='ne, ni [m^-3]',
                                style='r-', line_desc='ne')



            if more_plots:
                for var, marker, label in zip(ni, markers[:len(ni)], labels):
                    self.fill_subplot(this_ax, r, var, x_label='r [m]', y_label='ne, ni [m^-3]',
                                    style='g{}'.format(marker), line_desc='ni {}'.format(label))
            else:
                self.fill_subplot(this_ax, r, ni, x_label='r [m]', y_label='ne, ni [m^-3]',
                                    style='g-', line_desc='ni ')
        except AttributeError:
            pass

        if only_densities:
            plt.show()
            return

        if only_potential:
            this_ax = ax
        elif only_densities or only_electrons or only_ions:
            this_ax = None
        else:
            this_ax = ax[1, 0]

        try:
            if more_plots:
                lnss, labss = [], []
                ax2 = this_ax.twinx()
                for var1, var2, marker, label in zip(phi, er, markers[:len(phi)], labels):
                    lns, labs = self.fill_subplot_twinx(this_ax, ax2, r, (var1,var2),
                                                        x_label = 'r [m]', y_label=('phi [V]', 'er [V/m]'),
                                                        style=('b{}'.format(marker), 'r{}'.format(marker)),
                                                        line_desc=('phi {}'.format(label), 'er {}'.format(label)))
                    lnss.extend(lns)
                    labss.extend(labs)

                this_ax.legend(lnss, labss, loc='best')
            else:
                ax2 = this_ax.twinx()
                lns, labs = self.fill_subplot_twinx(this_ax, ax2, r, (phi,er),
                                                    x_label = 'r [m]', y_label=('phi [V]', 'er [V/m]'),
                                                    style=('b-', 'r-'), line_desc=('phi', 'er'))
                this_ax.legend(lns, labs, loc='best')
        except AttributeError:
            pass

        if only_potential:
            plt.show()
            return

        if only_electrons:
            this_ax = ax
        elif only_densities or only_potential or only_ions:
            this_ax = None
        else:
            this_ax = ax[0, 1]

        try:
            if more_plots:
                lnss, labss = [], []
                ax2 = this_ax.twinx()
                for var1, var2, marker, label in zip(Te, vre, markers[:len(phi)], labels):
                    lns, labs = self.fill_subplot_twinx(this_ax, ax2, r, (var1, var2),
                                                        x_label = 'r [m]', y_label=('Te', 'vre'),
                                                        style=('c{}'.format(marker), 'm{}'.format(marker)),
                                                        line_desc=('Te {}'.format(label), 'vre {}'.format(label)))
                    lnss.extend(lns)
                    labss.extend(labs)

                this_ax.legend(lnss, labss, loc='best')
            else:
                ax2 = this_ax.twinx()
                lns, labs = self.fill_subplot_twinx(this_ax, ax2, r, (Te, vre),
                                                    x_label = 'r [m]', y_label=('Te', 'vre'),
                                                    style=('c-', 'm-'), line_desc=('Te', 'vre'))
                this_ax.legend(lns, labs, loc='best')
        except AttributeError:
            pass

        if only_electrons:
            plt.show()
            return

        if only_ions:
            this_ax = ax
        elif only_densities or only_potential or only_ions:
            this_ax = None
        else:
            this_ax = ax[1, 1]

        try:
            if more_plots:
                lnss, labss = [], []
                ax2 = this_ax.twinx()
                for var1, var2, marker, label in zip(Ti, vri, markers[:len(phi)], labels):
                    lns, labs = self.fill_subplot_twinx(this_ax, ax2, r, (var1, var2),
                                                        x_label = 'r [m]', y_label=('Ti', 'vri'),
                                                        style=('c{}'.format(marker), 'm{}'.format(marker)),
                                                        line_desc=('Ti {}'.format(label), 'vri {}'.format(label)))
                    lnss.extend(lns)
                    labss.extend(labs)

                this_ax.legend(lnss, labss, loc='best')
            else:
                ax2 = this_ax.twinx()
                lns, labs = self.fill_subplot_twinx(this_ax, ax2, r, (Ti, vri),
                                                    x_label = 'r [m]', y_label=('Ti', 'vri'),
                                                    style=('c-', 'm-'), line_desc=('Ti', 'vri'))
                this_ax.legend(lns, labs, loc='best')
        except AttributeError:
            pass

        if only_ions:
            plt.show()
            return

        plt.show()

    def blot_averaged_profiles(self, ts_from=1, ts_to=-1, stddev=False):
        """
        Pops up an interactive plot of averaged profiles over specified time interval.

        Args:
            ts_from (int) - number of timestep to average from
            ts_to (int) - number of timestep to average to
        """

        index_from = self.timestep2dataindex(ts_from)
        index_to = self.timestep2dataindex(ts_to)
        averaged_profiles = self.average_profiles(index_from, index_to)

        r = self.r_grid[0]
        ne = averaged_profiles['ne']
        ni = averaged_profiles['ni']
        phi = averaged_profiles['phi']
        er = averaged_profiles['er']
        Te = averaged_profiles['Te']
        vre = averaged_profiles['vre']
        Ti = averaged_profiles['Ti']
        vri = averaged_profiles['vri']
        ne_stddev = averaged_profiles['ne_stddev']
        ni_stddev = averaged_profiles['ni_stddev']

        s1 = bfigure(width=850, plot_height=400, title = None, x_axis_label="r [m]", y_axis_label="n_e, n_i [m^-3]")
        s1.y_range = Range1d(start=ne[np.nanargmin(ne[0:-1])+1]*0.97,end=ne[np.nanargmax(ne[0:-1])+1]*1.03)
        s1.line(r, ne[0:-1], line_width=1, color="red")
        s1.line(r, ni[0:-1], line_width=1, color="green")

        s2 = bfigure(width=850, plot_height=400, title = None, x_axis_label="r [m]", y_axis_label="phi [V]")
        s2.y_range = Range1d(start=phi[np.nanargmin(phi[0:-1])+1]*0.97,end=phi[np.nanargmax(phi[0:-1])+1]*1.03)
        s2.line(r, phi[0:-1], line_width=1, color="red")
        s2.extra_y_ranges = {"Er": Range1d(start=er[np.nanargmin(er[0:-1])+1]*0.97,end=er[np.nanargmax(er[0:-1])+1]*1.03)}
        s2.line(r, er[0:-1], line_width=1, color="blue", y_range_name="Er")
        s2.add_layout(LinearAxis(y_range_name="Er",axis_label="Er [V/m]"), 'right')

        s3 = bfigure(width=850, plot_height=400, title = "electron", x_axis_label="r [m]", y_axis_label="Te [K]")
        s3.y_range = Range1d(start=Te[np.nanargmin(Te[0:-1])+1]*0.97,end=Te[np.nanargmax(Te[0:-1])+1]*1.03)
        s3.line(r, Te[0:-1], line_width=1, color="blue")
        s3.extra_y_ranges = {"vre": Range1d(start=vre[np.nanargmin(vre[0:-1])+1]*0.97,end=vre[np.nanargmax(vre[0:-1])+1]*1.03)}
        s3.line(r, vre[0:-1], line_width=1, color="purple", y_range_name="vre")
        s3.add_layout(LinearAxis(y_range_name="vre",axis_label="vre [m/s]"), 'right')

        s4 = bfigure(width=850, plot_height=400, title = "ion", x_axis_label="r [m]", y_axis_label="Ti [K]")
        s4.y_range = Range1d(start=Ti[np.nanargmin(Ti[0:-1])+1]*0.97,end=Ti[np.nanargmax(Ti[0:-1])+1]*1.03)
        s4.line(r, Ti[0:-1], line_width=1, color="blue")
        s4.extra_y_ranges = {"vri": Range1d(start=vri[np.nanargmin(vri[0:-1])+1]*0.97,end=vri[np.nanargmax(vri[0:-1])+1]*1.03)}
        s4.line(r, vri[0:-1], line_width=1, color="purple", y_range_name="vri")
        s4.add_layout(LinearAxis(y_range_name="vri",axis_label="vri [m/s]"), 'right')

        if stddev:
            x_band = np.append(r, r[::-1])
            ne_band = np.append(ne+ne_stddev, ne[::-1]-ne_stddev[::-1])
            ni_band = np.append(ni+ni_stddev, ni[::-1]-ni_stddev[::-1])
            s1.patch(x_band, ne_band, fill_alpha=0.2, color="red", line_color="white")
            s1.patch(x_band, ni_band, fill_alpha=0.2, color="green", line_color="white")

        p = vplot(s1, s2, s3, s4)

        bshow(p)


    def test_particles_save(self, no_run):
        """
        Tests particles' saves and inits. Basically, subsequent groups init_*
        and save_* should be the same but the dimensions
        """
        save_attrs = self.get_attrs_as_dict(self.saves[no_run])
        init_attrs = self.get_attrs_as_dict(self.inits[no_run+1])

        all_ok = True
        test_keys = ['itime', 'nprobe_tmp_Electron', 'nprobe_tmp_ArgonIon', 'nsheath_tmp_Electron',
                     'nsheath_tmp_ArgonIon', 'NNew_electron_tmp', 'NNew_ArgonIon_tmp', 'sweep_rest',
                    ]
        for key in test_keys:
            try:
                comparison = save_attrs[key] == init_attrs[key]
                logger.debug('key %s compared - %s', key, comparison)
                logger.debug('init: %s, save: %s', init_attrs[key], save_attrs[key])
                all_ok = all_ok and comparison
            except KeyError:
                logger.debug('cant compare %s, missing in one of attrs', key)

        logger.debug('ALL ATTRS TEST: %s', all_ok)

        ari_is_there = self.h5_f[self.saves[no_run]]['ari_is_there'][...]
        el_is_there = self.h5_f[self.saves[no_run]]['el_is_there'][...]

        mask_ari = ari_is_there == 1
        mask_el = el_is_there == 1

        dataset_to_test = 'ari_is_there'
        logger.debug('testing %s', dataset_to_test)
        self._test_particles_save_one(no_run, dataset_to_test)

        dataset_to_test = 'el_is_there'
        logger.debug('testing %s', dataset_to_test)
        self._test_particles_save_one(no_run, dataset_to_test)

        tests_ari = ['ari_vx', 'ari_vy', 'ari_vz', 'ari_x', 'ari_y', 'ari_z', 'ari_time_rest', 'ari_tau_c']
        tests_el = ['el_vx', 'el_vy', 'el_vz', 'el_x', 'el_y', 'el_z', 'el_time_rest', 'el_tau_c']

        for test_ari, test_el in zip(tests_ari, tests_el):
            logger.debug('testing %s', test_ari)
            self._test_particles_save_one(no_run, test_ari, mask=mask_ari)

            logger.debug('testing %s', test_el)
            self._test_particles_save_one(no_run, test_el, mask=mask_el)


    def _test_particles_save_one(self, no_run, dataset_name, mask=None):
        array1 = self.h5_f[self.saves[no_run]][dataset_name][...]
        array2 = self.h5_f[self.inits[no_run+1]][dataset_name][...]

        if mask is None:
            logger.debug('sum1: {}, sum2: {}'.format(np.sum(array1), np.sum(array2)))
            assert np.allclose([np.sum(array1)], [np.sum(array2)], atol=1e-10, rtol=1e-10),\
                   '{}: sum1: {}, sum2: {}'.format(dataset_name, np.sum(array1), np.sum(array2))
        else:
            logger.debug('sum1: {}, sum2: {}'.format(np.sum(array1[mask]), np.sum(array2)))
            assert np.allclose([np.sum(array1[mask])], [np.sum(array2)], atol=1e-10, rtol=1e-8),\
                   '{}: sum1: {}, sum2: {}'.format(dataset_name, np.sum(array1), np.sum(array2))


    def test_stats(self):
        """
        This test can be ran only with special type of output data. To test whether gstats are really
        sum of all lstats, we need to have all lstats. Therefore, run simulation with out_every = 1 and
        every_ion = 1. Run the simulation only once and on these data run this test.
        """
        to_test = ['ari_num', 'el_num', 'ari_v2', 'el_v2', 'ari_vr', 'el_vr', 'ari_vr2', 'el_vr2',
                   'ari_vx', 'el_vx', 'ari_vy', 'el_vy', 'ari_vz', 'el_vz']
        for test in to_test:
            logger.debug('testing {}'.format(test))
            g = self.h5_f['/{}/gstat_{}'.format(self.gstats[0], test)][...]
            l = self.h5_f['/{}/lstat_{}'.format(self.data[1], test)][...]
            max_ts = max(self.data.keys())
            for ts in xrange(2, max_ts+1):
                l += self.h5_f['/{}/lstat_{}'.format(self.data[ts], test)][...]

        assert np.allclose(g, l), '{} g: {}, l: {}'.format(test, g, l)

