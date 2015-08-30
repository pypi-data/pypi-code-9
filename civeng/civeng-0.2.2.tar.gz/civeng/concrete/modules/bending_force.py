
from ..cat262 import Beton, Betonstahl
from ..params import dm_set, epsilon_c2d, epsilon_ud
from math import pi, sqrt
from ...results import Results


def as_(dm, s):
	term = dm**2*pi/4*1000/s
	return term

class BendingForce(Results):
	standard = 'SH+BB 08'
	pick = ['mrd', 'as_min', 'epsilon_s_inf']

	def __init__(self, entries):
		Results.__init__(self)

		self.beton = Beton(entries['beton'], entries['gamma_c'])
		self.betonstahl = Betonstahl(entries['betonstahl'], entries['gamma_s'])
		self.fcd = self.beton.fcd()
		self.fsd = self.betonstahl.fsd()

		dm_inf = dm_set[entries['dm_inf']]
		s_inf = entries['s_inf']
		self.as_inf = as_(dm_inf, s_inf)
		self.d_inf = int(entries['d_inf'])

		self.w = int(entries['w'])
		self.h = int(entries['h'])
		self.fctd = self.beton.fctd(self.w, self.h)
		

		self.results = {}

	def compute(self):
		if self.w > 0 and self.h > 0 and self.d_inf > 0:
			x = self.x()
			self.mrd(x)
			self.epsilon_s_inf(x)
			self.xd(x)
			self.zd(x)
			self.mrd_()
			self.as_min()
			self.mrd_max_stat_d()
			self.mrd_max_stat_ind()
			self.as_max_stat_d()
			self.as_max_stat_ind()

		self.resultsf.update(self.beton.get_results())
		self.resultsf.update(self.betonstahl.get_results())
		# return [self.results[k] for k in order_qick], self.results
		return  [], self.sorted_results(), self.quick_results(self.pick)

	def epsilon_s_inf(self, x):
		term = epsilon_c2d/x*(self.d_inf-x)
		check = round(term/epsilon_ud, 1)
		self.add_rslt('epsilon_s_inf', round(term*1e3, 2), '&epsilon;.s,inf', '\u2030')
		return term

	def x(self):
		term = self.as_inf*self.fsd/(0.85*self.w*self.fcd)
		self.add_rslt('x', round(term), 'x', 'mm')
		return term

	def z(self, x):
		term = self.d_inf-0.425*x
		self.add_rslt('z', round(term), 'z', 'mm')
		return term

	def mrd(self, x):
		term = self.as_inf*self.fsd*self.z(x)
		check = round(term/self.mrd_max_stat_d(), 1)
		self.results['mrd'] = (round(term*1e-6, 1), 'M.Rd', 'kNm')
		self.add_rslt('mrd', round(term*1e-6, 1), 'M.Rd', 'kNm')
		return term

	def xd(self, x):
		term = x/self.d_inf
		self.add_rslt('xd', round(term, 2), 'x/d', '-')
		return term

	def zd(self, x):
		term = self.z(x)/self.d_inf
		self.add_rslt('zd', round(term, 2), 'z/d', '-')
		return term

	def mrd_(self):
		term = self.fctd*self.w*self.h**2/6
		self.add_rslt('mrd_', round(term*1e-6, 1), 'M.rd', 'kNm')
		return term

	def as_min(self):
		term = self.w*self.fcd/self.fsd*(self.d_inf-sqrt(self.d_inf**2-self.fctd*self.h**2/(3*self.fcd)))
		check = round(term/self.as_inf, 1)
		self.add_rslt('as_min', round(term, 1), 'A.s,min', 'mm^2')
		return term

	def mrd_max_stat_d(self):
		xd = 0.35
		term = 0.85*xd*self.w*self.fcd*self.d_inf**2*(1-0.425*xd)
		self.add_rslt('mrd_max_stat', round(term*1e-6, 1), 'M.Rd,max,0.35', 'kNm')
		return term

	def mrd_max_stat_ind(self):
		xd = 0.5
		term = 0.85*xd*self.w*self.fcd*self.d_inf**2*(1-0.425*xd)
		self.add_rslt('mrd_max_stat_ind', round(term*1e-6, 1), 'M.Rd,max,0.5', 'kNm')
		return term

	def as_max_stat_d(self):
		xd = 0.35
		term = 0.85*xd*self.w*self.fcd*self.d_inf/self.fsd
		self.add_rslt('as_max_stat_d', round(term), 'A.s,max,0.35', 'mm^2')
		return term

	def as_max_stat_ind(self):
		xd = 0.5
		term = 0.85*xd*self.w*self.fcd*self.d_inf/self.fsd
		self.add_rslt('as_max_stat', round(term), 'A.s,max,0.5', 'mm^2')
		return term

