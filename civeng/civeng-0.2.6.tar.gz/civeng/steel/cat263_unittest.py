
import unittest
from civeng.steel.cat263 import Cat263, MCR, MDRd, NkRd

printr = True

def printf(test, results):
	print('### {} ###'.format(test))
	for r in results['main_rslts']:
		print('{}: {}'.format(r['name'], r['result']))


class Cat263Test(unittest.TestCase):
	
	def setUp(self):
		self.entries = {
			'steel_grade': 'S 235', 
			'shape': 'IPE', 
			'size': '80'
		}
		self.ved = 5
		print('setUp executed!')
	
	def testCalculation(self):
		cat263 = Cat263(self.entries)
		
		self.assertEqual(round(cat263.nrd()*1e-3), 171)
		self.assertEqual(round(cat263.mrdy()*1e-6, 1), 5.2)
		self.assertEqual(round(cat263.mrdz()*1e-6, 1), 1.3)
		self.assertEqual(round(cat263.vrd()*1e-3, 1), 46)
		self.assertGreater(round(cat263.mvrd(self.ved)*1e-6), 0)
		
		cat263.get_results()

	def tearDown(self):
		print("tearDown executed!")

class MDRdTest(unittest.TestCase):
	"""SIA 263:13, 4.5.2 Kippen von Biegeträgern
	C4/06, 3.2 Anwendungsbeispiel zum Kippnachweis
	"""

	def setUp(self):
		self.entries = {
			'steel_grade': 'S 235',
			'shape': 'IPE',
			'size': '600',
			'psi': 0.5,
			'ld': 4000,
			'production': 'rolled',
			'w': 'wply',
			'sub_code': 'sia263e',
			
		}

	def testCalculation(self):
		mcr = MCR(self.entries)  # requires ld, psi
		self.assertEqual(round(mcr.eta(), 2), 1.30)
		self.assertEqual(round(mcr.i('double_symmetric')), 56)
		self.assertEqual(round(mcr.sigma_dw()), 528)
		self.assertEqual(round(mcr.c()), 998000)
		self.assertEqual(round(mcr.sigma_dv()), 324)
		self.assertEqual(round(mcr.sigma_crd()), 620)
		printf('MCR', mcr.get_results())
		
		mdrd = MDRd(self.entries)
		self.assertEqual(mdrd.alpha_d(), 0.21)
		self.assertEqual(round(mdrd.lambda_d_(), 3), 0.659)
		self.assertEqual(round(mdrd.chi_d(), 4), 0.9169)

		print('mdrd: {}'.format(mdrd.mdrd()))
		printf('MdRd', mdrd.get_results())

class NKRdTest(unittest.TestCase):
	"""SIA 263:13, 4.5.1 Knicken
	C4/06, 2.2 Anwendungsbeispiel
	"""
	
	def setUp(self):
		self.entries = {
			'steel_grade': 'S 275',
			'shape': 'HEA',
			'size': '180',
			'lk': 4000,  # [mm]
			'ned': 400,  # [kN]
			'production': 'rolled',
		}

	def testCalculation(self):
		nkrd = NkRd(self.entries)
		self.assertEqual(nkrd.alpha('z'), 0.49)
		self.assertEqual(round(nkrd.lambda_k_z(), 2), 1.02)
		self.assertEqual(round(nkrd.nkrd_z()*1e-3, 0), 627)
		print('NkRd: {}'.format(nkrd.phi_k_z()))
		print('NkRd: {}'.format(nkrd.chi_k_z()))
		print('NkRd: {}'.format(nkrd.nkrd_z()))
		printf('NkRd', nkrd.get_results())



if __name__ == "__main__":
	unittest.main() 
