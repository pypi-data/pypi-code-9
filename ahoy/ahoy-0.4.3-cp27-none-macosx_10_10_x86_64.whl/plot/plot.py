from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from ciabatta.ejm_rcparams import reds_cmap
from agaro import output_utils
from ahoy.utils import utils
from ahoy.plot.var_plot import VarPlot
import ahoy.fields


def plot_2d(dirname):
    fig = plt.figure()
    ax_vis = fig.add_subplot(111)

    fnames = output_utils.get_filenames(dirname)
    m_0 = output_utils.filename_to_model(fnames[0])

    L = m_0.ships.agents.positions.L

    ax_vis.set_xlim(-L[0] / 2.0, L[0] / 2.0)
    ax_vis.set_ylim(-L[1] / 2.0, L[1] / 2.0)
    ax_vis.set_aspect('equal')

    plt.subplots_adjust(left=0.25, bottom=0.25)
    has_c_field = isinstance(m_0.ships.c_field, ahoy.fields.FoodField)
    if has_c_field:
        plot_c = VarPlot(m_0.ships.c_field.c, cmap=reds_cmap, axes=ax_vis)
    plot_p = ax_vis.quiver(m_0.ships.agents.positions.r_w[:, 0],
                           m_0.ships.agents.positions.r_w[:, 1],
                           m_0.ships.agents.directions.u[:, 0],
                           m_0.ships.agents.directions.u[:, 1])

    ax_slide = plt.axes([0.25, 0.1, 0.65, 0.03])
    t_slider = Slider(ax_slide, 'Time', 0, len(fnames), valinit=0)

    t_time = fig.text(0.1, 0.5, '')

    def update(val):
        fname_i = int(round(val))
        if 0 <= fname_i < len(fnames):
            m = output_utils.filename_to_model(fnames[fname_i])
            if has_c_field:
                plot_c.update(m.ships.c_field.c)
            plot_p.set_offsets(m.ships.agents.positions.r_w)
            plot_p.set_UVC(m.ships.agents.directions.u[:, 0],
                           m.ships.agents.directions.u[:, 1])
            t_time.set_text('Time: {:g}'.format(m.ships.time.t))

            fig.canvas.draw_idle()

    t_slider.on_changed(update)

    plt.show()


def plot_linear_density(dirname):
    fig = plt.figure()
    ax_d = fig.add_subplot(211)
    ax_c = fig.add_subplot(212)

    fnames = output_utils.get_filenames(dirname)
    m_0 = output_utils.filename_to_model(fnames[0])

    L = m_0.ships.agents.positions.L

    dx = L[0] / 100.0

    plt.subplots_adjust(left=0.25, bottom=0.25)

    ds, xbs = utils.get_linear_density(m_0, dx)

    plot_d = ax_d.bar(xbs[:-1], ds, width=xbs[1] - xbs[0])
    c_field = m_0.ships.c_field.c
    plot_c = ax_c.scatter(c_field.mesh.cellCenters[0, :], c_field.value)
    ax_slide = plt.axes([0.25, 0.1, 0.65, 0.03])
    t_slider = Slider(ax_slide, 'Index', 0, len(fnames), valinit=0)

    ax_d.set_xlim(-L[0] / 2.0, L[0] / 2.0)
    ax_c.set_xlim(-L[0] / 2.0, L[0] / 2.0)
    ax_c.set_ylim(0.0, m_0.ships.c_field.c_0)

    def update(val):
        fname_i = int(round(val))
        if 0 <= fname_i < len(fnames):
            m = output_utils.filename_to_model(fnames[fname_i])
            ds, xbs = utils.get_linear_density(m, dx)
            for rect, d in zip(plot_d, ds):
                rect.set_height(d)
            c_field = m.ships.c_field.c
            plot_c.set_offsets(np.array([c_field.mesh.cellCenters[0, :],
                                         c_field.value]).T)
            fig.canvas.draw_idle()

    t_slider.on_changed(update)

    plt.show()


def plot_1d(dirname):
    fig = plt.figure()
    ax_vis = fig.add_subplot(211)
    ax_d = fig.add_subplot(212)

    fnames = output_utils.get_filenames(dirname)
    m_0 = output_utils.filename_to_model(fnames[0])

    L = m_0.ships.agents.positions.L

    ax_vis.set_xlim(-L[0] / 2.0, L[0] / 2.0)
    ax_d.set_xlim(-L[0] / 2.0, L[0] / 2.0)

    dx = L / 100.0

    plt.subplots_adjust(left=0.25, bottom=0.25)
    plot_p = ax_vis.scatter(m_0.ships.agents.positions.r_w[:, 0],
                            np.zeros([m_0.ships.agents.n]))

    d = m_0.ships.agents.positions.get_density_field(dx)
    x = np.linspace(-L[0] / 2.0, L[0] / 2.0, d.shape[0])

    plot_d = ax_d.bar(x, d, width=x[1] - x[0])

    ax_slide = plt.axes([0.25, 0.1, 0.65, 0.03])
    t_slider = Slider(ax_slide, 'Index', 0, len(fnames), valinit=0)

    def update(val):
        fname_i = int(round(val))
        if 0 <= fname_i < len(fnames):
            m = output_utils.filename_to_model(fnames[fname_i])
            plot_p.set_offsets(np.array([m.ships.agents.positions.r_w[:, 0],
                                         np.zeros([m.ships.agents.n])]).T)
            ds = m.ships.agents.positions.get_density_field(dx)
            for rect, d in zip(plot_d, ds):
                rect.set_height(d)
            ax_d.set_ylim(0.0, 1.05 * ds.max())
            fig.canvas.draw_idle()

    t_slider.on_changed(update)

    plt.show()


def plot_vis(dirname):
    dim = output_utils.get_recent_model(dirname).ships.dim
    if dim == 1:
        plot_1d(dirname)
    elif dim == 2:
        plot_2d(dirname)


def plot_t_uds_scalar(dirname, ax):
    ts, uds = utils.t_uds_scalar(dirname)
    ax.plot(ts, uds)


def plot_t_uds_vector(dirname, ax):
    ts, uds = utils.t_uds_vector(dirname)
    for vd_set in uds.T:
        ax.plot(ts, vd_set)


def plot_t_Ds_scalar(dirname, ax):
    ts, Ds = utils.t_Ds_scalar(dirname)
    ax.plot(ts, Ds)


def plot_t_Ds_vector(dirname, ax):
    ts, Ds = utils.t_Ds_vector(dirname)
    for D_set in Ds.T:
        ax.plot(ts, D_set)


def plot_t_rs_scalar(dirname, ax):
    ts, rs = utils.t_rs_scalar(dirname)
    ax.plot(ts, rs)


def plot_t_rs_vector(dirname, ax):
    ts, rs = utils.t_rs_vector(dirname)
    for r_set in rs.T:
        ax.plot(ts, r_set)


def plot_t_u_nets_scalar(dirname, ax):
    ts, u_nets = utils.t_u_nets_scalar(dirname)
    ax.plot(ts, u_nets)


def plot_t_u_nets_vector(dirname, ax):
    ts, u_nets = utils.t_u_nets_vector(dirname)
    for u_net_set in u_nets.T:
        ax.plot(ts, u_net_set)


def plot_chi_uds_x(dirnames, ax):
    chis, uds = utils.chi_uds_x(dirnames)
    i_sort = np.argsort(chis)
    chis, uds = chis[i_sort], uds[i_sort]
    ax.scatter(chis, uds)
    ax.set_xlim(-0.02, 1.0)
    ax.set_ylim(0.0, 1.1)


def plot_pf_Ds_scalar(dirnames, ax):
    pfs, Ds = utils.pf_Ds_scalar(dirnames)
    i_sort = np.argsort(pfs)
    pfs, Ds = pfs[i_sort], Ds[i_sort]
    ax.scatter(pfs, Ds)
    ax.set_xlim(-0.02, 1.0)
    ax.set_ylim(0.0, 410.0)


def plot_pf_uds_x(dirnames, ax):
    pfs, uds = utils.pf_uds_x(dirnames)
    i_sort = np.argsort(pfs)
    pfs, uds = pfs[i_sort], uds[i_sort]
    ax.scatter(pfs, uds / uds[0])
    ax.set_xlim(-0.02, 1.0)
    ax.set_ylim(0.0, 1.01)


def plot_pf_duds_x(dirnames, ax):
    pfs, uds = utils.pf_uds_x(dirnames)
    i_sort = np.argsort(pfs)
    pfs, uds = pfs[i_sort], uds[i_sort]
    uds_norm = uds / uds[0]
    duds = np.diff(uds_norm) / pfs[:-1]
    ax.scatter(pfs[:-1], duds)
    ax.set_xlim(-0.02, 1.0)
    # ax.set_ylim(0.0, 1.0)


def plot_Dr_0_Ds_scalar(dirnames, ax):
    Dr_0s, Ds = utils.Dr_0_Ds_scalar(dirnames)
    i_sort = np.argsort(Dr_0s)
    Dr_0s, Ds = Dr_0s[i_sort], Ds[i_sort]
    ax.scatter(Dr_0s, Ds)
    # ax.set_xlim(-0.02, 1.0)
    # ax.set_ylim(0.0, 410.0)
    ax.set_xscale('log')
    ax.set_yscale('log')


def plot_p_0_Ds_scalar(dirnames, ax):
    p_0s, Ds = utils.p_0_Ds_scalar(dirnames)
    i_sort = np.argsort(p_0s)
    p_0s, Ds = p_0s[i_sort], Ds[i_sort]
    ax.scatter(p_0s, Ds)
    # ax.set_xlim(-0.02, 1.0)
    # ax.set_ylim(0.0, 410.0)
    ax.set_xscale('log')
    ax.set_yscale('log')


def plot_th_density(ds, th_bins, fig):
    ax = plt.subplot(111, polar=True)
    dth = th_bins[1] - th_bins[0]
    ax.plot(th_bins[:-1], ds * dth)
    ax.set_rmax(1.0)
    ax.grid(True)
