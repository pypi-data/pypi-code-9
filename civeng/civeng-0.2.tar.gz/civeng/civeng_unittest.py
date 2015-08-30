
import unittest
from civeng.concrete.modules.bending_force import BendingForce
from civeng.concrete.params import gamma_c, eta_t, gamma_s, dm, s


class BendingForceTest(unittest.TestCase):
	
	def setUp(self):
		self.entries = {
			'beton': (3, 3),
			'gamma_c': (gamma_c, gamma_c),
			'eta_t': (eta_t, eta_t),
			'betonstahl': (0, 0),
			'gamma_s': (gamma_s, gamma_s),
			'dm_inf': (dm, dm),
			's_inf:': (s, s),
			'w': (1000, 1000),
			'h': (250, 300),
			'd_inf': (210, 260),
			}
		print('setUp executed!')
	
	def testCalculation(self):
		
		for i in range(len(self.entries['beton'])):
			entries = {}
			for k, v in self.entries.items():
				entries[k] = v[i]
			
			biegung = BendingForce(entries)
			for v in biegung.compute():
				print(v)


if __name__ == "__main__":
	unittest.main()

