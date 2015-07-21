from ase.qmmm import QMMMCalculator
from ase.calculators.emt import EMT
from ase import Atoms
h = Atoms('H2', positions=[[0, 0, 0], [0, 0, 0.5]])
h.calc = EMT()
print(h.get_forces())
h.calc = QMMMCalculator([0], EMT(), EMT(), EMT())
print(h.get_forces())
print(h.calc.calculate_numerical_forces(h))
from gpaw import GPAW
h.calc = QMMMCalculator([0], GPAW(mode='lcao'), EMT(), EMT(), vacuum=2.5)
print(h.get_forces())
