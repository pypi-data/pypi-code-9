
from collections import OrderedDict

# 3.2.2.1

rho = 7850  # kg/m3
e = 210*1e3  # N/mm2
g = 81*1e3  # N/mm2
v = 0.3

# 3.2.2.2
alpha_t = 10*10-6  # /°C

# 3.2.2.3

steel_grade_dict = OrderedDict([
    ('S 235', ((235, 135, 360), (215, 124, 340))),
    ('S 275', ((275, 160, 255), (430, 147, 410))),
    ('S 355', ((355, 205, 510), (335, 193, 490))),
    ('S 460', ((460, 265, 550), (248, 430, 530))),
])

# 4.1.3

gamma_m1 = 1.05
gamma_m2 = 1.25

cross_section_classes = ('1 + 2', '3', '4')