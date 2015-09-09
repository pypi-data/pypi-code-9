import numpy as np

default_model_kwargs = {
    'seed': 1,
    'dim': 2,
    'dt': 0.01,
    'n': 5000,
    'v_0': 20.0,
    'dt_mem': 0.1,
    't_mem': 5.0,
    'pore_R': 30.0,
    'L': np.array([300.0, 300.0]),
    'Dr_0': 1.0,
    'p_0': 1.0,
}

combo_to_chi = {
    ('Dr_0', False, False): 0.38747846573137146,
    ('Dr_0', False, True): 0.91610356364005729,
    ('Dr_0', True, False): 0.55171912452935623,
    ('Dr_0', True, True): 0.95031324074045198,
    ('p_0', False, False): 0.38527303561393739,
    ('p_0', False, True): 0.85519056757936063,
    ('p_0', True, False): 0.54788034865582758,
    ('p_0', True, True): 0.88731933438050015
}
