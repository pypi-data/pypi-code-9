
import unittest

from civeng.concrete.modules.bending_force import BendingForce, BendingCompression


class BendingForceTest(unittest.TestCase):
	
	def setUp(self):
		self.entries = {
			'beton': 3,
			'gamma_c': 1.5,
			'eta_t': 1.0,
			'betonstahl': 0,
			'gamma_s': 1.15,
			'as_inf': {'dm': 10, 's': 150, 'd':210},
 			'w': 1000,
			'h': 250,
			'd_inf': 260,
			}
		print('setUp executed!')
	
	def testCalculation(self):
		
		biegung = BendingForce(self.entries)
		#print(biegung.compute())

class BendingCompressionTest(unittest.TestCase):
	
	def setUp(self):
		self.entries = {
			'beton': 3,
			'gamma_c': 1.5,
			'eta_t': 1.0,
			'betonstahl': 0,
			'gamma_s': 1.15,
			'as_sup': {'dm': 3, 's': 333, 'd':40},
			'as_inf': {'dm': 4, 's': 200, 'd':410},
			'w': 300,
			'h': 450,
			}
		print('setUp executed!')

	def testCalculation(self):
		b = BendingCompression(self.entries)
		print('{}'.format(b.compute()))



if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest(BendingCompressionTest('testCalculation'))
	unittest.TextTestRunner().run(suite)
	


