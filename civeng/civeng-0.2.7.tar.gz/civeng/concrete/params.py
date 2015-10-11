
from collections import OrderedDict

# 2.3.2.6
gamma_c = 1.5
gamma_s = 1.15


# 4.2.1.3
eta_t = 1.0
eta_t_set = (0.85, 1.0, 1.2)

# 4.2.1.4
epsilon_c1d = 0.002
epsilon_c2d = 0.003


# 4.2.1.16
gamma_ce = 1.0

# 4.2.3.1
epsilon_ud = 0.020

roh = 2200  # in kg/m3

ke = 10000



kc = 0.55
kc_set = (1.0, 0.8, 0.55, 0.4)

dmax = 32  # in mm
dmax_set = (32, 16, 8)

alpha = 45
alpha_set = (30, 25, 40)

beta = 90

beton_dict = OrderedDict([  # ('Type', (fck, fctm, beta_fc)),
    ('C 12/15', (12, 1.6, 3.8)),
    ('C 16/20', (16, 1.9, 3.4)),
    ('C 20/25', (20, 2.2, 3.2)),
    ('C 25/30', (25, 2.6, 2.9)),
    ('C 30/37', (30, 2.9, 2.7)),
    ('C 35/45', (35, 3.2, 2.6)),
    ('C 40/50', (40, 3.5, 2.4)),
    ('C 45/55', (45, 3.8, 2.3)),
    ('C 50/60', (50, 4.1, 2.2))
])

steel = OrderedDict([
    ('S 235', (235, 360, 215, 340)),
    ('S 275', (275, 430, 255, 410)),
    ('S 355', (355, 510, 335, 490)),
    ('S 460', (460, 550, 430, 530))
])

betonstahl_dict = OrderedDict([  # ('Type', (fsk, ks, epsilon_ud)),
    ('B500A', (500, 1.05, 0.020)),
    ('B500B', (500, 1.08, 0.045)),
    ('B500C', (500, 1.15, 0.065)),
    ('B700B', (700, 1.08, 0.045))
])
es = 205000  # N/mm2

values_prestressing_steel = OrderedDict([  # ('Type', OrderedDict([])),
    ('wires', OrderedDict([  # ('Type', (fpk, fp0,1k)),
        ('Y1860C-3,0', (1860, 1600)),
        ('Y1860C-4,0', (1860, 1600)),
        ('Y1860C-5,0', (1860, 1600))
    ])),
    ('strands', OrderedDict([
        ('Y1860S7-12,9', (1860, 1600)),
        ('Y1770S7-15,3', (1170, 1520)),
        ('Y1860S7-15,3', (1860, 1600))
    ])),
    ('bars', OrderedDict([
        ('Y1100H-20,0', (1100, 900)),
        ('Y1030H-26,0', (1030, 830)),
        ('Y1050C-26,0', (1050, 950))
    ])),
])

values_adhesive_reinforcement = OrderedDict([
    ('CFK', (2800, 165000))
])

values_adhesive_reinforcement_types = OrderedDict([
    ('', OrderedDict([
        ('', (0, 0))
    ])),
    ('CFK', OrderedDict([
        ('B5', (1.2, 50)),
        ('B8', (1.2, 80)),
        ('B10', (1.2, 100)),
        ('C6', (1.4, 60)),
        ('C9', (1.4, 90)),
        ('C10', (1.4, 100)),
        ('C12', (1.4, 120)),
        ('C15', (1.4, 150))
    ]))])

dm = 10
dm_set = (6, 8, 10, 12, 14, 16, 18, 20, 22, 26, 30, 34, 40)
s = 150
s_set = (500, 300, 250, 200, 150, 100, 75)


project_data = {
    'project': 'None',
    'info': 'None',
    'engineer': 'Studer Partner AG, Bauingenieure, 6206 Neuenkirch',
    'signature': 'mr',
    'path': 'None'
}


