from __future__ import print_function, division
import sys
import matplotlib.pyplot as plt
from ahoy.plot import plot


def plot_chi_uds_x():
    ax = plt.gca()
    plot.plot_chi_uds_x(sys.argv[1:], ax)
    plt.show()


def plot_Dr_0_Ds_scalar():
    ax = plt.gca()
    plot.plot_Dr_0_Ds_scalar(sys.argv[1:], ax)
    plt.show()


def plot_linear_density():
    ax = plt.gca()
    plot.plot_linear_density(sys.argv[1], ax)
    plt.show()


def plot_p_0_Ds_scalar():
    ax = plt.gca()
    plot.plot_p_0_Ds_scalar(sys.argv[1:], ax)
    plt.show()


def plot_pf_Ds_scalar():
    ax = plt.gca()
    plot.plot_pf_Ds_scalar(sys.argv[1:], ax)
    plt.show()


def plot_pf_uds_x():
    ax = plt.gca()
    plot.plot_pf_uds_x(sys.argv[1:], ax)
    plt.show()


def plot_t_Ds_scalar():
    ax = plt.gca()
    plot.plot_t_Ds_scalar(sys.argv[1], ax)
    plt.show()


def plot_t_Ds_vector():
    ax = plt.gca()
    plot.plot_t_Ds_vector(sys.argv[1], ax)
    plt.show()


def plot_t_rs_scalar():
    ax = plt.gca()
    plot.plot_t_rs_scalar(sys.argv[1], ax)
    plt.show()


def plot_t_rs_vector():
    ax = plt.gca()
    plot.plot_t_rs_vector(sys.argv[1], ax)
    plt.show()


def plot_t_u_nets_scalar():
    ax = plt.gca()
    plot.plot_t_u_nets_scalar(sys.argv[1], ax)
    plt.show()


def plot_t_u_nets_vector():
    ax = plt.gca()
    plot.plot_t_u_nets_vector(sys.argv[1], ax)
    plt.show()


def plot_t_uds_scalar():
    ax = plt.gca()
    plot.plot_t_uds_scalar(sys.argv[1], ax)
    plt.show()


def plot_t_uds_vector():
    ax = plt.gca()
    plot.plot_t_uds_vector(sys.argv[1], ax)
    plt.show()


def plot_vis():
    plot.plot_vis(sys.argv[1])
