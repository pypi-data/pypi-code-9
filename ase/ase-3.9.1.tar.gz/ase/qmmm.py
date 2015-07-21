from ase.calculators.calculator import Calculator


class QMMMCalculator(Calculator):
    implemented_properties = ['energy', 'forces']
    
    def __init__(self, selection, qmcalc, mmcalc1, mmcalc2, vacuum=None):
        self.selection = selection
        self.qmcalc = qmcalc
        self.mmcalc1 = mmcalc1
        self.mmcalc2 = mmcalc2
        self.vacuum = vacuum
        
        self.qmatoms = None
        self.center = None
        
        self.name = qmcalc.name + '+' + mmcalc1.name
        
        Calculator.__init__(self)
        
    def initialize_qm(self, atoms):
        self.qmatoms = atoms[self.selection]
        self.qmatoms.pbc = False
        if self.vacuum:
            self.qmatoms.center(vacuum=self.vacuum)
            self.center = self.qmatoms.positions.mean(axis=0)
            
    def calculate(self, atoms, properties, system_changes):
        Calculator.calculate(self, atoms, properties, system_changes)
        
        if self.qmatoms is None:
            self.initialize_qm(atoms)
            
        self.qmatoms.positions = atoms.positions[self.selection]
        if self.vacuum:
            self.qmatoms.positions += (self.center -
                                       self.qmatoms.positions.mean(axis=0))
            
        energy = self.mmcalc2.get_potential_energy(atoms)
        forces = self.mmcalc2.get_forces(atoms)
        
        energy += self.qmcalc.get_potential_energy(self.qmatoms)
        qmforces = self.qmcalc.get_forces(self.qmatoms)
        if self.vacuum:
            qmforces -= qmforces.mean(axis=0)
        forces[self.selection] += qmforces
        
        energy -= self.mmcalc1.get_potential_energy(self.qmatoms)
        forces[self.selection] -= self.mmcalc1.get_forces(self.qmatoms)

        self.results['energy'] = energy
        self.results['forces'] = forces
