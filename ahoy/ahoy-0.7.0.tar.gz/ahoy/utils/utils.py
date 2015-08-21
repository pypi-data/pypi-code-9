from __future__ import print_function, division
import numpy as np
from scipy.stats import sem
from agaro.output_utils import get_recent_model
from agaro.measure_utils import measures, t_measures, params


def seg_intersect(p1, p2, yi):
    x1, y1 = p1
    x2, y2 = p2
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    xi = (yi - c) / m
    if x1 < xi < x2:
        return xi
    else:
        raise ValueError


def curve_intersect(xs, ys, yi):
    i_big = np.where(ys > yi)[0][0]
    p1 = [xs[i_big - 1], ys[i_big - 1]]
    p2 = [xs[i_big], ys[i_big]]
    return seg_intersect(p1, p2, yi)


def get_vd_coeff(x, t):
    return x / t


def get_diff_coeff(x, t):
    return x ** 2 / (2.0 * t)


# Measure getters


def get_ud_vector(m):
    dr = m.ships.agents.positions.dr
    uds = get_vd_coeff(dr, m.ships.time.t) / m.ships.agents.swimmers.v_0
    return np.mean(uds, axis=0), sem(uds, axis=0)


def get_ud_scalar(m):
    dr = m.ships.agents.positions.dr_mag
    uds = get_vd_coeff(dr, m.ships.time.t) / m.ships.agents.swimmers.v_0
    return np.mean(uds, axis=0), sem(uds, axis=0)


def get_D_vector(m):
    dr = m.ships.agents.positions.dr
    Ds = get_diff_coeff(dr, m.ships.time.t)
    return np.mean(Ds, axis=0), sem(Ds, axis=0)


def get_D_scalar(m):
    dr = m.ships.agents.positions.dr_mag
    Ds = get_diff_coeff(dr, m.ships.time.t)
    return np.mean(Ds, axis=0), sem(Ds, axis=0)


def get_r_vector(m):
    dr = m.ships.agents.positions.dr
    return np.mean(dr, axis=0), sem(dr, axis=0)


def get_r_scalar(m):
    dr = m.ships.agents.positions.dr_mag
    return np.mean(dr, axis=0), sem(dr, axis=0)


def get_u_net_vector(m):
    us = m.ships.agents.directions.u
    return np.mean(us, axis=0), sem(us, axis=0)


def get_u_net_scalar(m):
    u_net, u_net_err = get_u_net_vector(m)

    u_net_sq = np.square(u_net)
    u_net_sq_err = 2.0 * u_net * u_net_err

    u_net_mag_sq = np.sum(u_net_sq)
    u_net_mag_sq_err = np.sqrt(np.sum(np.square(u_net_sq_err)))

    u_net_mag = np.sqrt(u_net_mag_sq)
    u_net_mag_err = 0.5 * u_net_mag_sq_err / u_net_mag
    return u_net_mag, u_net_mag_err

# Parameter getters


def get_chi(m):
    return m.ships.agents.chi


def get_pf(m):
    return m.ships.obstructor.fraction_occupied


def get_Dr_0(m):
    return m.ships.agents.rudder_sets.Dr_0


def get_p_0(m):
    return m.ships.agents.rudder_sets.p_0


def get_noise_0_tot(m):
    return m.ships.agents.noise_0_tot


def get_time(m):
    return m.ships.time.t

# Time dependence


def t_uds_vector(dirname):
    """Calculate the particle drift speed over time along each axis
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    uds: numpy.ndarray[dtype=float]
         Drift speeds, normalised by the swimmer speed.
    """
    return t_measures(dirname, get_ud_vector)


def t_uds_scalar(dirname):
    """Calculate the overall particle drift speed over time
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    uds: numpy.ndarray[dtype=float]
         Particle drift speeds.
    """
    return t_measures(dirname, get_ud_scalar)


def t_Ds_scalar(dirname):
    """Calculate the overall particle diffusion constant over time
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    Ds: numpy.ndarray[dtype=float]
         Particle diffusion constants.
    """
    return t_measures(dirname, get_D_scalar)


def t_Ds_vector(dirname):
    """Calculate the particle diffusion constant over time along each axis
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    Ds: numpy.ndarray[dtype=float]
         Particle diffusion constants.
    """
    return t_measures(dirname, get_D_vector)


def t_rs_scalar(dirname):
    """Calculate the overall particle displacement over time
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    rs: numpy.ndarray[dtype=float]
         Particle diffusion constants.
    """
    return t_measures(dirname, get_r_scalar)


def t_rs_vector(dirname):
    """Calculate the particle displacement over time along each axis
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    rs: numpy.ndarray[dtype=float]
         Particle diffusion constants.
    """
    return t_measures(dirname, get_r_vector)


def t_u_nets_scalar(dirname):
    """Calculate the particles' overall centre-of-mass speed over time
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    v_nets: numpy.ndarray[dtype=float]
         Centre-of-mass particle speeds.
    """
    return t_measures(dirname, get_u_net_scalar)


def t_u_nets_vector(dirname):
    """Calculate the particle's centre-of-mass velocity over time
    for a model output directory.

    Parameters
    ----------
    dirname: str
        A model output directory path

    Returns
    -------
    ts: numpy.ndarray[dtype=float]
        Times.
    v_nets: numpy.ndarray[dtype=float]
         Centre-of-mass particle velocities.
    """
    return t_measures(dirname, get_u_net_vector)


# Parameter to measure relations


def chi_uds_x(dirnames, t_steady=None):
    chis = params(dirnames, get_chi)
    uds, uds_err = measures(dirnames, get_ud_vector, t_steady)
    return chis, uds[:, 0], uds_err[:, 0]


def pf_Ds_scalar(dirnames, t_steady=None):
    pfs = params(dirnames, get_pf)
    Ds, Ds_err = measures(dirnames, get_D_scalar, t_steady)
    return pfs, Ds, Ds_err


def pf_uds_x(dirnames, t_steady=None):
    pfs = params(dirnames, get_pf)
    uds, uds_err = measures(dirnames, get_ud_vector, t_steady)
    return pfs, uds[:, 0], uds_err[:, 0]


def Dr_0_Ds_scalar(dirnames, t_steady=None):
    Dr_0s = params(dirnames, get_Dr_0)
    Ds, Ds_err = measures(dirnames, get_D_scalar, t_steady)
    return Dr_0s, Ds, Ds_err


def p_0_Ds_scalar(dirnames, t_steady=None):
    p_0s = params(dirnames, get_p_0)
    Ds, Ds_err = measures(dirnames, get_D_scalar, t_steady)
    return p_0s, Ds, Ds_err


def noise_0_tot_Ds_scalar(dirnames, t_steady=None):
    noise_0_tots = params(dirnames, get_noise_0_tot)
    Ds, Ds_err = measures(dirnames, get_D_scalar, t_steady)
    return noise_0_tots, Ds, Ds_err


# Related to finding equivalent chis to give equal drift speeds


def get_equiv_chi(ud_0, dirnames):
    chis, uds, uds_err = chi_uds_x(dirnames)
    i_sort = np.argsort(chis)
    chis, uds, uds_err = chis[i_sort], uds[i_sort], uds_err[i_sort]
    return curve_intersect(chis, uds, ud_0)


def get_equiv_chi_key(m):
    noise_var_key = 'p_0' if m.ships.agents.does_tumbling else 'Dr_0'
    chemo_rudders = m.ships.agents.rudder_sets.chemo_rudders
    key = (noise_var_key, chemo_rudders.is_onesided,
           chemo_rudders.noise_measurer.is_temporal)
    return key


def get_equiv_chi_item(ud_0, dirnames):
    key = get_equiv_chi_key(get_recent_model(dirnames[0]))
    chi_equiv = get_equiv_chi(ud_0, dirnames)
    return key, chi_equiv


def get_equiv_chi_dict(ud_0, dirname_sets):
    params_to_chi = {}
    for dirnames in dirname_sets:
        key, chi_equiv = get_equiv_chi_item(ud_0, dirnames)
        params_to_chi[key] = chi_equiv
    return params_to_chi


# Density distributions


def circle_segment_angle(d, R):
    return 2.0 * np.arccos(d / R)


def circle_segment_area(d, R):
    if d > R:
        return 0.0
    elif d < -R:
        return np.pi * R ** 2.0
    else:
        theta = circle_segment_angle(d, R)
        return ((R ** 2) / 2.0) * (theta - np.sin(theta))


def circle_cross_section_area(d_1, d_2, R):
    return np.abs(circle_segment_area(d_1, R) - circle_segment_area(d_2, R))


def linear_areas(rs, R, Lx, Ly, nx):
    x = np.linspace(-Lx / 2.0, Lx / 2.0, nx)
    linear_areas = np.full_like(x, Lx * Ly / nx)
    for i_r in range(rs.shape[0]):
        for i in range(nx - 1):
            d_1 = rs[i_r] - x[i]
            d_2 = rs[i_r] - x[i + 1]
            cross_section_area = circle_cross_section_area(d_1, d_2, R)
            linear_areas[i] -= cross_section_area
    return linear_areas


def linear_density(xs, xcs, R, Lx, Ly, dx):
    nx = int(round(Lx / dx))
    ns, x_bins = np.histogram(xs, bins=nx, range=(-Lx / 2.0, Lx / 2.0))
    areas = linear_areas(xcs, R, Lx, Ly, nx)
    densities = ns.astype(np.float) / areas
    return densities, x_bins


def get_linear_density(m, dx):
    xs = m.ships.agents.positions.r[:, 0]
    try:
        xcs = m.ships.obstructor.rs[:, 0]
        R = m.ships.obstructor.R
    except AttributeError:
        xcs = np.array([])
        R = 0.0
    Lx, Ly = m.ships.agents.positions.L
    return linear_density(xs, xcs, R, Lx, Ly, dx)


def angle_density(ths, dth):
    nth = int(round(2.0 * np.pi / dth))
    ns, th_bins = np.histogram(ths, bins=nth, range=(-np.pi, np.pi))
    dth = th_bins[1] - th_bins[0]
    densities = ns.astype(np.float) / (ns * dth).sum()
    return densities, th_bins


def get_angle_density(m, dth):
    ths = m.ships.agents.directions.th
    return angle_density(ths, dth)
