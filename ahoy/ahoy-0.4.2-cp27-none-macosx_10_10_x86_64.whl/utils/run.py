from __future__ import print_function, division
from itertools import product
import numpy as np
from agaro import run_utils
import ahoy.turners
from ahoy.model import Model
from ahoy.utils.defaults import default_model_kwargs, combo_to_chi


def run_spatial():
    extra_model_kwargs = {
        'n': 50000,
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': False,
        'pore_turner': ahoy.turners.AlignTurner(),
        'pore_pf': 0.0707,

        'tumble_flag': True,
        'tumble_chemo_flag': True,
        'onesided_flag': True,
        'chi': 0.5,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    model = Model(**model_kwargs)

    t_output_every = 50.0
    t_upto = 100.0
    output_dir = None
    force_resume = None

    run_utils.run_model(t_output_every, output_dir, m=model,
                        force_resume=force_resume, t_upto=t_upto)


def run_Dr_scan():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
        'pore_turner': ahoy.turners.BounceBackTurner(),
        'pore_pf': 0.8,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 5.0
    t_upto = 300.0
    Dr_0s = np.logspace(-2, 2, 9)
    force_resume = True
    parallel = True

    run_utils.run_field_scan(Model, model_kwargs,
                             t_output_every, t_upto, 'Dr_0', Dr_0s,
                             force_resume=force_resume, parallel=parallel)


def run_pf_scan():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
        'pore_turner': ahoy.turners.ReflectTurner(),
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 100.0
    t_upto = 500.0
    pfs = np.linspace(0.0, 0.8, 9)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    noise_vars = ['Dr_0', 'p_0']
    turners = [ahoy.turners.Turner(), ahoy.turners.BounceBackTurner(),
               ahoy.turners.ReflectTurner(), ahoy.turners.AlignTurner()]
    for noise_var, turner, pf in product(noise_vars, turners, pfs):
        model_kwargs_cur = model_kwargs.copy()
        if noise_var == 'Dr_0':
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
        model_kwargs_cur['pore_turner'] = turner
        model_kwargs_cur['pore_pf'] = pf
        model_kwarg_sets.append(model_kwargs_cur)

    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_chi_scan():
    extra_model_kwargs = {
        'spatial_flag': True,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 100.0
    t_upto = 200.0
    chis = np.linspace(0.0, 0.95, 3)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    dims = [1, 2]
    noise_vars = ['Dr_0', 'p_0']
    onesided_flags = [True, False]
    temporal_chemo_flags = [True, False]
    combos = product(noise_vars, dims, onesided_flags, temporal_chemo_flags,
                     chis)
    for noise_var, dim, onesided_flag, temporal_chemo_flag, chi in combos:
        model_kwargs_cur = model_kwargs.copy()
        if noise_var == 'Dr_0':
            if dim == 1:
                continue
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['rotation_chemo_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
            model_kwargs_cur['tumble_chemo_flag'] = False
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['rotation_chemo_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
            model_kwargs_cur['tumble_chemo_flag'] = True
        model_kwargs_cur['dim'] = dim
        model_kwargs_cur['onesided_flag'] = onesided_flag
        model_kwargs_cur['temporal_chemo_flag'] = temporal_chemo_flag
        model_kwargs_cur['chi'] = chi
        model_kwarg_sets.append(model_kwargs_cur)

    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_pf_scan_drift():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
        'pore_turner': ahoy.turners.AlignTurner(),
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 100.0
    t_upto = 500.0
    pore_pfs = np.linspace(0.0, 0.8, 11)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    noise_vars = ['Dr_0', 'p_0']
    onesided_flags = [True, False]
    temporal_chemo_flags = [True, False]
    combos = product(noise_vars, onesided_flags, temporal_chemo_flags, pfs)
    for noise_var, onesided_flag, temporal_chemo_flag, pf in combos:
        model_kwargs_cur = model_kwargs.copy()

        if noise_var == 'Dr_0':
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['rotation_chemo_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
            model_kwargs_cur['tumble_chemo_flag'] = False
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['rotation_chemo_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
            model_kwargs_cur['tumble_chemo_flag'] = True
        model_kwargs_cur['onesided_flag'] = onesided_flag
        model_kwargs_cur['temporal_chemo_flag'] = temporal_chemo_flag
        key = noise_var, onesided_flag, temporal_chemo_flag
        model_kwargs_cur['chi'] = combo_to_chi[key]
        model_kwargs_cur['pf'] = pf
        model_kwarg_sets.append(model_kwargs_cur)

    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_field():
    rho_0 = 0.1
    c_delta_0 = 0.1
    c_delta = c_delta_0 / rho_0

    extra_model_kwargs = {
        'rho_0': rho_0,

        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,

        'L': np.array([250.0, 200.0]),
        'origin_flags': np.array([True, False]),

        'pore_turner': ahoy.turners.AlignTurner(),
        'pore_pf': 0.4,
        'pore_R': 20.0,

        'c_field_flag': True,
        'c_dx': 10.0,
        'c_D': 10.0,
        'c_delta': c_delta,
        'c_0': 1.0,

        'chi': 15.0,
        'p_0': 1.0,
        'tumble_chemo_flag': True,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    model = Model(**model_kwargs)

    t_output_every = 0.1
    t_upto = 5.0
    output_dir = None
    force_resume = None

    run_utils.run_model(t_output_every, output_dir, m=model,
                        force_resume=force_resume, t_upto=t_upto)
