from __future__ import absolute_import
import logging
import sys
from .sim_process import SimProcess
import matplotlib.pyplot as plt
import boltons
from probe.params import SimParams
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
#matplotlib.rcParams['text.usetex']=True
#matplotlib.rcParams['text.latex.unicode']=True

from bokeh.io import vplot
from bokeh.io import show as bshow
from bokeh.plotting import figure as bfigure

logger = logging.Logger('NULL')
logger.addHandler(logging.NullHandler())

cfg = {'debug' : 2}

class MultiLineFormatter(logging.Formatter):

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

def berrorbar(fig, x, y, xerr=None, yerr=None, color='blue', point_kwargs={}, error_kwargs={}):
    #Tohle se bude moct oddelat az konecne bokeh prida errorbary
    fig.circle(x, y, color=color, **point_kwargs)

    if xerr is not None:
        x_err_x = []
        x_err_y = []
        for px, py, err in zip(x, y, xerr):
            x_err_x.append((px - err, px + err))
            x_err_y.append((py, py))
        fig.multi_line(x_err_x, x_err_y, color=color, **error_kwargs)

    if yerr is not None:
        y_err_x = []
        y_err_y = []
        for px, py, err in zip(x, y, yerr):
            y_err_x.append((px, px))
            y_err_y.append((py - err, py + err))
        fig.multi_line(y_err_x, y_err_y, color=color, **error_kwargs)

class SimManager(object):

    def __init__(self, h5_paths_dict):

        """
        This object can handle a compare results from multiple simulations.

        It should be initialized by a dictionary, where key is a short description
        of the simluation and a value is a path to h5 file with results.
        """

        self.h5_paths_dict = h5_paths_dict
        logger.debug('self.h5_paths_dict: %s', self.h5_paths_dict)

        self.sim_processes = dict()
        for desc, path_to_h5 in self.h5_paths_dict.iteritems():
            logger.info('initializing sim_process, desc: %s, path: %s', desc, path_to_h5)
            self.sim_processes[desc] = SimProcess(path_to_h5)

    def parse_fit_from_to(self, fit_from, fit_to):

        if fit_from is not None:
            fit_from_dict = self.parse_ts_from_to(fit_from)
            logger.debug('fit_from_dict: %s', fit_from_dict)
        else:
            fit_from_dict = dict(zip(self.sim_processes.keys(),
                                     [1]*len(self.sim_processes)))

        if fit_to is not None:
            fit_to_dict = self.parse_ts_from_to(fit_to)
            logger.debug('fit_to_dict: %s', fit_to_dict)
        else:
            fit_to_dict = dict(zip(self.sim_processes.keys(),
                                   [-1]*len(self.sim_processes)))

        return fit_from_dict, fit_to_dict


    def plot_current_summary(self, fit_from=None, fit_to=None,
                             model_points=1000, figsize=(25, 13),
                             dependence_on='r_d', font_size=20,
                             major_tick_size=12, minor_tick_size=8, legend=True,
                             filename=None):

        fit_results = self.stats_constants_models('current', fit_from=fit_from,
                                                  fit_to=fit_to,
                                                  model_points=model_points)

        fig = plt.figure(figsize=figsize)
        OML_simple = dict()
        for desc, sp in self.sim_processes.iteritems():
            sim_param = SimParams(dict_with_params=sp.params[0])
            particle = 'electron' if sp.params[0]['phi_p'] > 0.0 else 'argon_ion'
            OML_simple[desc] = sim_param.OML_simplified(particle)
        ax = plt.subplot2grid((1, 1), (0, 0))
        #_, ax = plt.subplots(figsize=figsize)
        x = list()
        y = list()
        yerr = list()
        for desc, fit_result in fit_results.iteritems():
            model, x_all, y_all, model_x, model_y = fit_result
            print desc
            print model.summary()
            print 'y = {} +- {}'.format(model.params[0], model.bse[0])
            x.append(self.sim_processes[desc].params[0][dependence_on])
            y.append(model.params[0])
            yerr.append(model.bse[0])

        ax.errorbar(x, y, yerr=yerr, fmt='o')
        x_min = min(x)*0.99
        x_max = max(x)*1.01
        ax.set_xlim(x_min, x_max)

        for desc, OML_current in OML_simple.iteritems():
            ax.plot([x_min, x_max], [-OML_current, -OML_current], label='{} OMLsimple'.format(desc))
        if legend:
            ax.legend(loc='best')
        ax.set_ylabel(r'Current $[\mathsf{A}]$', fontsize=font_size)
        #ax.set_xlabel(dependence_on, fontsize=font_size)
        ax.set_xlabel(r"Domain radius $[\mathsf{m}]$", fontsize=font_size)
        ax.tick_params(axis='both', which='major', labelsize=major_tick_size)
        ax.tick_params(axis='both', which='minor', labelsize=minor_tick_size)

        if filename is None:
            plt.show()
        else:
            plt.tight_layout()
            fig.savefig(filename, format="eps", dpi=1000)


    def blot_current_summary(self, fit_from=None, fit_to=None,
                             model_points=1000, dependence_on='r_d'):

        p = bfigure(width=850, height=400)
        p.xaxis.axis_label = dependence_on
        p.yaxis.axis_label = "current [A]"

        fit_results = self.stats_constants_models('current', fit_from=fit_from,
                                                      fit_to=fit_to,
                                                      model_points=model_points)

        OML_simple = dict()
        for desc, sp in self.sim_processes.iteritems():
            sim_param = SimParams(dict_with_params=sp.params[0])
            particle = 'electron' if sp.params[0]['phi_p'] > 0.0 else 'argon_ion'
            OML_simple[desc] = sim_param.OML_simplified(particle)

        x = list()
        y = list()
        yerr = list()

        for desc, fit_result in fit_results.iteritems():
            model, x_all, y_all, model_x, model_y = fit_result
            print desc
            print model.summary()
            print 'y = {} +- {}'.format(model.params[0], model.bse[0])
            x.append(self.sim_processes[desc].params[0][dependence_on])
            y.append(model.params[0])
            yerr.append(model.bse[0])

        berrorbar(p, x, y, yerr=yerr)

        x_min = min(x)*0.99
        x_max = max(x)*1.01

        for desc, OML_current in OML_simple.iteritems():
            p.line([x_min, x_max], [-OML_current, -OML_current], color="red")

        bshow(p)

    def stats_constants_models(self, variable, fit_from=None, fit_to=None,
                               model_points=1000):

        fit_from_dict, fit_to_dict = self.parse_fit_from_to(fit_from, fit_to)

        fit_results = dict()
        for desc, sp in self.sim_processes.iteritems():
            fit_results[desc] = sp.stats_constant_model(variable,
                                                        ts_from=fit_from_dict[desc],
                                                        ts_to=fit_to_dict[desc],
                                                        model_points=model_points)

        return fit_results

    def plot_stats_constants_models(self, variable, fit_from=None, fit_to=None,
                                    figsize=(25, 13), model_points=1000):

        fit_results = self.stats_constants_models(variable, fit_from=fit_from,
                                                  fit_to=fit_to,
                                                  model_points=model_points)

        _, ax = plt.subplots(figsize=figsize)
        for desc, fit_result in fit_results.iteritems():
            model, x_all, y_all, model_x, model_y = fit_result
            print desc
            print model.summary()
            print 'y = {} +- {}'.format(model.params[0], model.bse[0])
            print
            ax.plot(x_all, y_all, label='{} data'.format(desc))
            label = '{} fit y = {} +- {}'.format(desc, model.params[0], model.bse[0])
            ax.plot(model_x, model_y, label=label)

        ax.legend(loc='best')
        plt.show()

    def blot_stats_constants_models(self, variable, fit_from=None,
                                    fit_to=None, model_points=1000):
        bcolors = ["red", "darkred", "blue", "navy", "limegreen", "darkgreen", "yellow", "olive", "magenta", "purple", "orange", "saddlebrown"]
        p = bfigure(width=850, height=400)

        fit_results = self.stats_constants_models(variable, fit_from=fit_from,
                                            fit_to=fit_to,
                                            model_points=model_points)
        color_id=0
        for desc, fit_result in fit_results.iteritems():
            model, x_all, y_all, model_x, model_y = fit_result
            print desc
            print model.summary()
            print 'y = {} +- {}'.format(model.params[0], model.bse[0])
            print

            p.line (x_all, y_all, legend='{} data'.format(desc), color=bcolors[color_id])
            label = '{} fit y = {} +- {}'.format(desc, model.params[0], model.bse[0])
            p.line(model_x, model_y, legend=label, line_dash=[4, 4], color=bcolors[color_id+1], line_width=2.5)
            color_id+=2

        bshow(p)

    def parse_ts_from_to(self, ts):
        if isinstance(ts, int):
            ts_dict = dict()
            for desc, _ in self.h5_paths_dict.iteritems():
                ts_dict[desc] = ts
        elif isinstance(ts, dict):
            ts_dict = ts
        elif isinstance(ts, list) or isinstance(ts, tuple):
            ts_dict = dict()

            c = 0
            for desc, _ in self.h5_paths_dict.iteritems():
                ts_dict[desc] = ts[c]
                c += 1

            print ts_dict
        else:
            raise ValueError('ts_from must be integer, dict, list or tuple, see docstring')

        return ts_dict


    def plot_averaged_profiles(self, plot_variable='n', ts_from=1, ts_to=-1, scale_by_rd=False,
                               filename=None, y_scale_by=1.0, y_scale_label='',
                               x_scale_by=1.0, x_scale_label='', ylabel='density',
                               xlabel='r', x_unit='m',
                               y_unit=r'm^{-3}', ions_on_secondary=False,
                               figsize=(25, 13), n_infty=None, stddev=False,
                               only_electrons=False, only_ions=False,
                               only_everything=False, font_size=28,
                               major_tick_size=16, minor_tick_size=8,
                               xlim=None, ylim=None, ylim2=None, pad=5,
                               border_thickness=0.1, linewidth=1.0):
        """
        plot averaged profiles of all simulations

        arguments:

        ts_from     should be either integer (average all simulation from that ts)
                    or dict (keys are same strings as in h5_paths_dict in __init__)
        ts_to       similar to ts_from
        """
        assert plot_variable in ['n', 'T']
        everything = False

        if plot_variable == 'n':
            plot_el = 'ne'
            plot_ion = 'ni'
            plot_el_dev = 'ne_stddev'
            plot_ion_dev = 'ni_stddev'

        if plot_variable == 'T':
            plot_el = 'Te'
            plot_ion = 'Ti'
            plot_el_dev = 'Te_stddev'
            plot_ion_dev = 'Ti_stddev'

        is_iterable = boltons.iterutils.is_iterable

        if is_iterable(ts_from):
            index_from = {label: self.sim_processes[label].timestep2dataindex(ts_f) for label, ts_f in ts_from.iteritems()}
        else:
            index_from = {label: self.sim_processes[label].timestep2dataindex(ts_from) for label in self.sim_processes.iterkeys()}

        if is_iterable(ts_to):
            index_to = {label: self.sim_processes[label].timestep2dataindex(ts_t) for label, ts_t in ts_to.iteritems()}
        else:
            index_to = {label: self.sim_processes[label].timestep2dataindex(ts_to) for label in self.sim_processes.iterkeys()}

        assert set(index_from.keys()) == set(index_to.keys())

        print 'averaging profiles'
        averaged_profiles = dict()
        for desc in index_from.iterkeys():
            averaged_profiles[desc] = self.sim_processes[desc].average_profiles(index_from[desc],
                                                                                index_to[desc],
                                                                               )
        print 'profiles averaged'

#        logger.debug('averaged_profiles: %s', averaged_profiles)
        fig = plt.figure(figsize=figsize)
        if everything:
            ax_el = plt.subplot2grid((2, 2), (0, 0))
            ax_ion = plt.subplot2grid((2, 2), (0, 1))
            ax_all = plt.subplot2grid((2, 2), (1, 0), colspan=2)
            #fig.tight_layout()

            for desc in averaged_profiles.iterkeys():
                if scale_by_rd:
                    if stddev:
                        ax_el.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_el],
                                    label='{} el'.format(desc), linewidth=linewidth)
                        ax_el.fill_between(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                           averaged_profiles[desc][plot_el]-averaged_profiles[desc][plot_el_dev],
                                           averaged_profiles[desc][plot_el]+averaged_profiles[desc][plot_el_dev]
                                          )

                    else:
                        ax_el.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_el],
                                    label='{} el'.format(desc), linewidth=linewidth)
                else:
                    if stddev:
                        ax_el.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_el],
                                    label='{} el'.format(desc), linewidth=linewidth)
                        ax_el.fill_between(self.sim_processes[desc].r_grid[0],
                                           averaged_profiles[desc][plot_el]-averaged_profiles[desc][plot_el_dev],
                                           averaged_profiles[desc][plot_el]+averaged_profiles[desc][plot_el_dev]
                                          )
                    else:
                        ax_el.plot(self.sim_processes[desc].r_grid[0],
                                   averaged_profiles[desc][plot_el],
                                   label='{} el'.format(desc), linewidth=linewidth)

            ax_el.legend(loc='best')

            for desc in averaged_profiles.iterkeys():
                if scale_by_rd:
                    if stddev:
                        ax_ion.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)
                        ax_ion.fill_between(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                           averaged_profiles[desc][plot_ion]-averaged_profiles[desc][plot_ion_dev],
                                           averaged_profiles[desc][plot_ion]+averaged_profiles[desc][plot_ion_dev]
                                          )
                    else:
                        ax_ion.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)
                else:
                    if stddev:
                        ax_ion.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)
                        ax_ion.fill_between(self.sim_processes[desc].r_grid[0],
                                           averaged_profiles[desc][plot_ion]-averaged_profiles[desc][plot_ion_dev],
                                           averaged_profiles[desc][plot_ion]+averaged_profiles[desc][plot_ion_dev]
                                          )
                    else:
                        ax_ion.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)

            ax_ion.legend(loc='best')

            for desc in averaged_profiles.iterkeys():
                if scale_by_rd:
                    if stddev:
                        ax_all.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_el],
                                    label='{} el'.format(desc), linewidth=linewidth)
                        ax_all.fill_between(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                           averaged_profiles[desc][plot_el]-averaged_profiles[desc][plot_el_dev],
                                           averaged_profiles[desc][plot_el]+averaged_profiles[desc][plot_el_dev]
                                          )
                        ax_all.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)
                        ax_all.fill_between(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                           averaged_profiles[desc][plot_ion]-averaged_profiles[desc][plot_ion_dev],
                                           averaged_profiles[desc][plot_ion]+averaged_profiles[desc][plot_ion_dev]
                                          )
                    else:
                        ax_all.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_el],
                                    label='{} el'.format(desc), linewidth=linewidth)
                        ax_all.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)
                else:
                    if stddev:
                        ax_all.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_el],
                                    label='{} el'.format(desc), linewidth=linewidth)
                        ax_all.fill_between(self.sim_processes[desc].r_grid[0],
                                           averaged_profiles[desc][plot_el]-averaged_profiles[desc][plot_el_dev],
                                           averaged_profiles[desc][plot_el]+averaged_profiles[desc][plot_el_dev]
                                          )
                        ax_all.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_ion],
                                    label='{} ion'.format(desc), linewidth=linewidth)
                        ax_all.fill_between(self.sim_processes[desc].r_grid[0],
                                           averaged_profiles[desc][plot_ion]-averaged_profiles[desc][plot_ion_dev],
                                           averaged_profiles[desc][plot_ion]+averaged_profiles[desc][plot_ion_dev]
                                          )
                    else:
                        ax_all.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_el], label='{} el'.format(desc), linewidth=linewidth)
                        ax_all.plot(self.sim_processes[desc].r_grid[0],
                                    averaged_profiles[desc][plot_ion], label='{} ion'.format(desc), linewidth=linewidth)

            ax_all.legend(loc='best')

        if only_everything:
            ax = plt.subplot2grid((1, 1), (0, 0), colspan=2)
            if ions_on_secondary:
                ax_el = ax
                ax_ion = ax.twinx()
            else:
                ax_el = ax
                ax_ion = ax

            lnss, labss = [], []
            for desc in averaged_profiles.iterkeys():
                if scale_by_rd:
                    if stddev:
                        if not only_ions:
                            lns = ax_el.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                            averaged_profiles[desc][plot_el] * y_scale_by, 'r-',
                                            label='{} el'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)

                            ax_el.fill_between(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                            averaged_profiles[desc][plot_el]*y_scale_by-averaged_profiles[desc][plot_el_dev]*y_scale_by,
                                            averaged_profiles[desc][plot_el]*y_scale_by+averaged_profiles[desc][plot_el_dev]*y_scale_by,
                                            facecolor='red'
                                            )

                        if not only_electrons:
                            lns = ax_ion.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                            averaged_profiles[desc][plot_ion]*y_scale_by, 'g-',
                                            label='{} ion'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)

                            ax_ion.fill_between(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                            averaged_profiles[desc][plot_ion]*y_scale_by-averaged_profiles[desc][plot_ion_dev]*y_scale_by,
                                            averaged_profiles[desc][plot_ion]*y_scale_by+averaged_profiles[desc][plot_ion_dev*y_scale_by],
                                            facecolor='green'
                                            )
                    else:
                        if not only_ions:
                            lns = ax_el.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                            averaged_profiles[desc][plot_el]*y_scale_by, 'r-',
                                            label='{} el'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)

                        if not only_electrons:
                            lns = ax_ion.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                            averaged_profiles[desc][plot_ion]*y_scale_by, 'g-',
                                            label='{} ion'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)
                else:
                    if stddev:
                        if not only_ions:
                            lns = ax_el.plot(self.sim_processes[desc].r_grid[0]*x_scale_by,
                                            averaged_profiles[desc][plot_el]*y_scale_by, 'r-',
                                            label='{} el'.format(desc), linewidth=linewidth)

                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)
                            ax_el.fill_between(self.sim_processes[desc].r_grid[0]*x_scale_by,
                                            averaged_profiles[desc][plot_el]*y_scale_by-averaged_profiles[desc][plot_el_dev]*y_scale_by,
                                            averaged_profiles[desc][plot_el]*y_scale_by+averaged_profiles[desc][plot_el_dev]*y_scale_by,
                                            facecolor='red'
                                            )
                        if not only_electrons:
                            lns = ax_ion.plot(self.sim_processes[desc].r_grid[0]*x_scale_by,
                                            averaged_profiles[desc][plot_ion]*y_scale_by, 'g-',
                                            label='{} ion'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)
                            ax_ion.fill_between(self.sim_processes[desc].r_grid[0]*x_scale_by,
                                                averaged_profiles[desc][plot_ion]*y_scale_by-averaged_profiles[desc][plot_ion_dev]*y_scale_by,
                                                averaged_profiles[desc][plot_ion]*y_scale_by+averaged_profiles[desc][plot_ion_dev]*y_scale_by,
                                                facecolor='green'
                                            )
                    else:
                        if not only_ions:
                            lns = ax_el.plot(self.sim_processes[desc].r_grid[0]*x_scale_by,
    #                                         averaged_profiles[desc][plot_el]*y_scale_by, 'r-',
                                            averaged_profiles[desc][plot_el]*y_scale_by,
                                            label='{} el'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)

                        if not only_electrons:
                            lns = ax_ion.plot(self.sim_processes[desc].r_grid[0]*x_scale_by,
    #                                          averaged_profiles[desc][plot_ion]*y_scale_by, 'g-',
                                            averaged_profiles[desc][plot_ion]*y_scale_by,
                                            label='{} ion'.format(desc), linewidth=linewidth)
                            labs = lns[0].get_label()
                            lnss.extend(lns); labss.append(labs)

            if xlim:
                ax_el.set_xlim(xlim)
                ax_ion.set_xlim(xlim)
            if ylim:
                ax_el.set_ylim(ylim)
                ax_ion.set_ylim(ylim2)

            ax_el.tick_params(direction='inout', pad=pad)
            ax_ion.tick_params(direction='inout', pad=pad)

            [i.set_linewidth(border_thickness) for i in ax_el.spines.itervalues()]
            [i.set_linewidth(border_thickness) for i in ax_ion.spines.itervalues()]

            ax.set_ylabel(ylabel + r' $[\mathsf{' + y_scale_label + ' ' + y_unit + r'}]$', fontsize=font_size)
            ax.set_xlabel(xlabel + r' $[\mathsf{' + x_scale_label + ' ' + x_unit + r'}]$', fontsize=font_size)
            ax_el.tick_params(axis='both', which='major', labelsize=major_tick_size)
            ax_el.tick_params(axis='both', which='minor', labelsize=minor_tick_size)
            ax_ion.tick_params(axis='both', which='major', labelsize=major_tick_size)
            ax_ion.tick_params(axis='both', which='minor', labelsize=minor_tick_size)
            ax.legend(lnss, labss, loc='best', fontsize=font_size)


        if n_infty and everything:
            ax_el.plot([self.sim_processes[desc].params[0]['r_p']*x_scale_by, self.sim_processes[desc].params[0]['r_d']*x_scale_by],
                       [n_infty*y_scale_by, n_infty*y_scale_by])
            ax_ion.plot([self.sim_processes[desc].params[0]['r_p']*x_scale_by, self.sim_processes[desc].params[0]['r_d']*x_scale_by],
                       [n_infty*y_scale_by, n_infty*y_scale_by])
            ax_all.plot([self.sim_processes[desc].params[0]['r_p']*x_scale_by, self.sim_processes[desc].params[0]['r_d']*x_scale_by],
                       [n_infty*y_scale_by, n_infty*y_scale_by])
        if n_infty and only_everything:
            ax.plot([self.sim_processes[desc].params[0]['r_p']*x_scale_by, self.sim_processes[desc].params[0]['r_d']*x_scale_by],
                    [n_infty*y_scale_by, n_infty*y_scale_by], 'k:')
        if n_infty and only_electrons:
            ax_el.plot([self.sim_processes[desc].params[0]['r_p']*x_scale_by, self.sim_processes[desc].params[0]['r_d']*x_scale_by],
                       [n_infty*y_scale_by, n_infty*y_scale_by], 'k:')
        if n_infty and only_ions:
            ax_ion.plot([self.sim_processes[desc].params[0]['r_p']*x_scale_by, self.sim_processes[desc].params[0]['r_d']*x_scale_by],
                       [n_infty*y_scale_by, n_infty*y_scale_by])

        if filename is None:
            plt.show()
        else:
            plt.tight_layout()
            fig.savefig(filename, dpi=1000)

    def blot_averaged_profiles(self, ts_from=1, ts_to=-1, scale_by_rd=False, filename=None,
                               figsize=(25, 13), n_infty=None, stddev=False):
        """
        plot averaged profiles of all simulations

        arguments:

        ts_from     should be either integer (average all simulation from that ts)
                    or dict (keys are same strings as in h5_paths_dict in __init__)
        ts_to       similar to ts_from
        """

        el_colors=["red", "darkred", "lightcoral", "orangered"]
        ion_colors=["green", "lime", "springgreen", "forestgreen"]

        s_ele = bfigure(width=850, height=400, title = "Electrons")
        s_ion = bfigure(width=850, height=400, title = "Ions")
        s_all = bfigure(width=850, height=400, title = "Everything")

        is_iterable = boltons.iterutils.is_iterable

        if is_iterable(ts_from):
            index_from = {label: self.sim_processes[label].timestep2dataindex(ts_f) for label, ts_f in ts_from.iteritems()}
        else:
            index_from = {label: self.sim_processes[label].timestep2dataindex(ts_from) for label in self.sim_processes.iterkeys()}

        if is_iterable(ts_to):
            index_to = {label: self.sim_processes[label].timestep2dataindex(ts_t) for label, ts_t in ts_to.iteritems()}
        else:
            index_to = {label: self.sim_processes[label].timestep2dataindex(ts_to) for label in self.sim_processes.iterkeys()}

        assert set(index_from.keys()) == set(index_to.keys())

        print 'averaging profiles'
        averaged_profiles = dict()
        for desc in index_from.iterkeys():
            averaged_profiles[desc] = self.sim_processes[desc].average_profiles(index_from[desc],
                                                                                index_to[desc],
                                                                               )
        print 'profiles averaged'

        color_id=0

        for desc in averaged_profiles.iterkeys():
            if scale_by_rd:
                if stddev:
                    s_ele.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                               averaged_profiles[desc]['ne'],
                               legend='{} el'.format(desc),
                               color=el_colors[color_id])
                    s_ele.patch(np.append(self.sim_processes[desc].r_grid[0] /
                                          self.sim_processes[desc].params[0]['r_d'],
                                          self.sim_processes[desc].r_grid[0][::-1]
                                          /
                                          self.sim_processes[desc].params[0]['r_d']),
                                np.append(averaged_profiles[desc]['ne']+averaged_profiles[desc]['ne_stddev'],
                                          averaged_profiles[desc]['ne'][::-1]-averaged_profiles[desc]['ne_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=el_colors[color_id])
                else:
                    s_ele.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                               averaged_profiles[desc]['ne'],
                               legend='{} el'.format(desc),
                               color=el_colors[color_id])
            else:
                if stddev:
                    s_ele.line(self.sim_processes[desc].r_grid[0],
                               averaged_profiles[desc]['ne'],
                               legend='{} el'.format(desc),
                               color=el_colors[color_id])
                    s_ele.patch(np.append(self.sim_processes[desc].r_grid[0],
                                          self.sim_processes[desc].r_grid[0][::-1]),
                                np.append(averaged_profiles[desc]['ne']+averaged_profiles[desc]['ne_stddev'],
                                          averaged_profiles[desc]['ne'][::-1]-averaged_profiles[desc]['ne_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=el_colors[color_id])
                else:
                    s_ele.line(self.sim_processes[desc].r_grid[0],
                               averaged_profiles[desc]['ne'],
                               legend='{} el'.format(desc),
                               color=el_colors[color_id])
            color_id+=1

        color_id=0
        for desc in averaged_profiles.iterkeys():
            if scale_by_rd:
                if stddev:
                   s_ion.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                               averaged_profiles[desc]['ni'],
                               legend='{} ion'.format(desc),
                               color=el_colors[color_id])
                   s_ion.patch(np.append(self.sim_processes[desc].r_grid[0] /
                                         self.sim_processes[desc].params[0]['r_d'],
                                         self.sim_processes[desc].r_grid[0][::-1]
                                         /
                                         self.sim_processes[desc].params[0]['r_d']),
                               np.append(averaged_profiles[desc]['ni']+averaged_profiles[desc]['ni_stddev'],
                                         averaged_profiles[desc]['ni'][::-1]-averaged_profiles[desc]['ni_stddev'][::-1]),
                               fill_alpha=0.2,
                               line_color="white", color=ion_colors[color_id])
                else:
                    s_ion.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                averaged_profiles[desc]['ni'],
                                legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
            else:
                if stddev:
                    s_ion.line(self.sim_processes[desc].r_grid[0],
                                averaged_profiles[desc]['ni'],
                                legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
                    s_ion.patch(np.append(self.sim_processes[desc].r_grid[0],
                                          self.sim_processes[desc].r_grid[0][::-1]),
                                np.append(averaged_profiles[desc]['ni']+averaged_profiles[desc]['ni_stddev'],
                                          averaged_profiles[desc]['ni'][::-1]-averaged_profiles[desc]['ni_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=ion_colors[color_id])
                else:
                    s_ion.line(self.sim_processes[desc].r_grid[0],
                                averaged_profiles[desc]['ni'],
                                legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
            color_id+=1

        color_id=0
        for desc in averaged_profiles.iterkeys():
            if scale_by_rd:
                if stddev:
                    s_all.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                averaged_profiles[desc]['ne'],
                                legend='{} el'.format(desc),
                                color=el_colors[color_id])
                    s_all.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                averaged_profiles[desc]['ni'],
                                legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
                    s_ele.patch(np.append(self.sim_processes[desc].r_grid[0] /
                                          self.sim_processes[desc].params[0]['r_d'],
                                          self.sim_processes[desc].r_grid[0][::-1]
                                          /
                                          self.sim_processes[desc].params[0]['r_d']),
                                np.append(averaged_profiles[desc]['ne']+averaged_profiles[desc]['ne_stddev'],
                                          averaged_profiles[desc]['ne'][::-1]-averaged_profiles[desc]['ne_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=el_colors[color_id])
                    s_ion.patch(np.append(self.sim_processes[desc].r_grid[0] /
                                          self.sim_processes[desc].params[0]['r_d'],
                                          self.sim_processes[desc].r_grid[0][::-1]
                                          /
                                          self.sim_processes[desc].params[0]['r_d']),
                                np.append(averaged_profiles[desc]['ni']+averaged_profiles[desc]['ni_stddev'],
                                          averaged_profiles[desc]['ni'][::-1]-averaged_profiles[desc]['ni_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=ion_colors[color_id])
                else:
                    s_all.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                averaged_profiles[desc]['ne'],
                                legend='{} el'.format(desc),
                                color=el_colors[color_id])
                    s_all.line(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                                averaged_profiles[desc]['ni'],
                                legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
            else:
                if stddev:
                    s_all.line(self.sim_processes[desc].r_grid[0],
                                averaged_profiles[desc]['ne'], legend='{} el'.format(desc),
                                color=el_colors[color_id])
                    s_all.line(self.sim_processes[desc].r_grid[0],
                                averaged_profiles[desc]['ni'], legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
                    s_all.patch(np.append(self.sim_processes[desc].r_grid[0],
                                          self.sim_processes[desc].r_grid[0][::-1]),
                                np.append(averaged_profiles[desc]['ne']+averaged_profiles[desc]['ne_stddev'],
                                          averaged_profiles[desc]['ne'][::-1]-averaged_profiles[desc]['ne_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=el_colors[color_id])
                    s_all.patch(np.append(self.sim_processes[desc].r_grid[0],
                                          self.sim_processes[desc].r_grid[0][::-1]),
                                np.append(averaged_profiles[desc]['ni']+averaged_profiles[desc]['ni_stddev'],
                                          averaged_profiles[desc]['ni'][::-1]-averaged_profiles[desc]['ni_stddev'][::-1]),
                                fill_alpha=0.2,
                                line_color="white", color=ion_colors[color_id])
                else:
                    s_all.line(self.sim_processes[desc].r_grid[0],
                                averaged_profiles[desc]['ne'], legend='{} el'.format(desc),
                                color=el_colors[color_id])
                    s_all.line(self.sim_processes[desc].r_grid[0],
                                averaged_profiles[desc]['ni'], legend='{} ion'.format(desc),
                                color=ion_colors[color_id])
            color_id+=1



        p=vplot(s_ele, s_ion, s_all)
        bshow(p)


