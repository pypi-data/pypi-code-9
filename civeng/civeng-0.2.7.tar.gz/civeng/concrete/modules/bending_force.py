
from math import fabs, sqrt
from ..cat262 import Beton, Betonstahl
from ..params import dm_set, epsilon_c2d, epsilon_ud, es
from ...funcs import as_
from ...results import Results




class BendingForceMain:
	def __init__(self, entries):
		self.entries = entries
		self.b_as_sup = entries['b_as_sup']
		self.b_as_sup1 = entries['b_as_sup1']

	def compute(self):
		if self.b_as_sup == False and self.b_as_sup1 == False:
			return BendingForce(self.entries).compute()
		elif self.b_as_sup == True or self.b_as_sup1 == False:
			return BendingCompression(self.entries).compute()
			


class BendingForce(Results):
	code = ''
	selection = ['mrd','mrd_max_stat_d', 'as_min', 'epsilon_s_inf', 'xd']

	def __init__(self, entries):

		self.concrete = Beton(entries['beton'], entries['gamma_c'])
		self.betonstahl = Betonstahl(entries['betonstahl'], entries['gamma_s'])
		self.fcd = self.concrete.fcd()
		self.fsd = self.betonstahl.fsd()

		#dm_inf = dm_set[entries['as_inf']['dm']]
		#s_inf = entries['as_inf']['s']
		self.as_inf = entries['as_inf']
		self.d_inf = entries['d_inf']

		self.w = int(entries['w'])
		self.h = int(entries['h'])
		self.fctd = self.concrete.fctd(self.w, self.h)

	def compute(self):
		if self.w > 0 and self.h > 0 and self.d_inf > 0:
			x = self.x()
			self.mrd()
			self.epsilon_s_inf(x)
			self.xd(x)
			self.zd(x)
			self.mrd_()
			self.as_min()
			self.mrd_max_stat_d()
			self.mrd_max_stat_ind()
			self.as_max_stat_d()
			self.as_max_stat_ind()

		return  self.get_results()

	def epsilon_s_inf(self, x):
		term = epsilon_c2d/x*(self.d_inf-x)
		epsilon_yd = self.betonstahl.epsilon_yd()
		self.add_rslt2(round(term*1e3, 2))
		return term

	def x(self):
		term = self.as_inf*self.fsd/(0.85*self.w*self.fcd)
		self.add_rslt('x', round(term), 'x', 'mm')
		return term

	def z(self, x):
		term = self.d_inf-0.425*x
		self.add_rslt('z', round(term), 'z', 'mm')
		return term

	def mrd(self):
		term = self.as_inf*self.fsd*self.z(self.x())
		check = round(term/self.mrd_max_stat_d(), 1)
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
		self.add_rslt('mrd_max_stat_d', round(term*1e-6, 1), 'M.Rd,max,0.35', 'kNm')
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
		self.add_rslt('as_max_stat_ind', round(term), 'A.s,max,0.5', 'mm^2')
		return term

from sympy.solvers import solve
from sympy import Symbol
from sympy.mpmath import findroot

class BendingCompression(Results):
	code = ''
	selection = ['x', 'mrd', 'epsilon_s_sup', 'epsilon_s_inf', 'xd', \
			  'zsd', 'dcd', 'dsd', 'sum']
	
	def __init__(self, entries):

		self.concrete = Beton(entries['beton'], entries['gamma_c'])
		self.betonstahl = Betonstahl(entries['betonstahl'], entries['gamma_s'])
		self.fcd = self.concrete.fcd()
		self.fsd = self.betonstahl.fsd()

		#dm_sup = dm_set[entries['as_sup']['dm']]
		#s_sup = entries['as_sup']['s']
		self.as_sup = entries['as_sup']
		self.d_sup= entries['d_sup']
		self.as_sup2 = entries['as_sup1']
		self.d_sup2 = entries['d_sup1']

		#dm_inf = dm_set[entries['as_inf']['dm']]
		#s_inf = entries['as_inf']['s']
		self.as_inf = entries['as_inf']
		self.d_inf = entries['d_inf']

		self.w = int(entries['w'])
		self.h = int(entries['h'])
		self.fctd = self.concrete.fctd(self.w, self.h)
		
		self.epsilon_yd = self.betonstahl.epsilon_yd()
		
	def compute(self):
		
		x = self.x_case()
		self.add_rslt('x', round(x[0]), 'x', 'mm')
		self.add_rslt('epsilon_s_sup', round(self.epsilon_s_sup(*x)*1e3, 3), 'essup', '-')
		self.add_rslt('epsilon_s_inf', round(self.epsilon_s_inf(x[0])*1e3, 3), 'esinf', '-')
		self.add_rslt('mrd', round(self.mrd_case(*x)*1e-6, 1), 'M.Rd', 'kNm')
		
		xd = round(x[0]/self.d_inf, 2)
		self.add_rslt('xd', xd, 'x/d', '-')
		if xd <= 0:
			self.add_msg('xd', 'xd <= 0')
		self.add_rslt('zsd', round(self.zsd()*1e-3, 1), 'Z.sd', 'kN')
		self.add_rslt('dcd', round(self.dcd(x[0])*1e-3, 1), 'D.cd', 'kN')
		self.add_rslt('dsd', round(self.dsd_case(*x)*1e-3, 1), 'D.sd', 'kN')
		check = self.zsd()+self.dcd(x[0])+self.dsd_case(*x)
		self.add_rslt('sum', round(check*1e-3, 1), '\u2211 = 0', 'kN')
		
		
		return self.get_results()
		

	def epsilon_s_inf(self, x):
		term = epsilon_c2d/x*(self.d_inf-x)
		return term

	def zsd(self):
		term = self.as_inf*self.fsd
		return term

	def dcd(self, x):
		term = -0.85*x*self.w*self.fcd
		return term

	# ds1d

	def epsilon_s_sup(self, x, flows):
		if flows:
			term = self.epsilon_yd
		else:
			term = epsilon_c2d/x*(x-self.d_sup)
		return term

	def sigma_s_sup(self, x, flows):
		term = self.epsilon_s_sup(x, flows)*es
		return term
	
	def dsd_case(self, x, flows):
		term = -self.as_sup*self.sigma_s_sup(x, flows)
		return term

	# end ds1d
	
	# ds2d
	
	def epsilon_s_sup2(self, x, flows):
		if flows:
			term = self.epsilon_yd
		else:
			term = epsilon_c2d/x*(x-self.d_sup2)
		return term

	def sigma_s_sup2(self, x, flows):
		term = self.epsilon_s_sup2(x, flows)*es
		return term

	def ds2d_case(self, x, flows):
		term = self.as_sup2*self.sigma_s_sup2(x, flows)
		return term 

	# end ds2d

	def x_case(self):

		flows = False

		while True:
			f = lambda x: self.zsd()+self.dsd_case(x, flows)+self.dcd(x)
			term = findroot(f, self.d_inf/2)

			if fabs(self.epsilon_s_sup(term, flows)) > self.epsilon_yd:
				flows = True
			else:
				return term, flows
				break

	def mrd_case(self, x, flows):
		term = self.dsd_case(x, flows)*(self.d_sup-self.h/2)+ \
			   self.dcd(x)*(0.425*x-self.h/2)+ \
		       self.zsd()*(self.d_inf-self.h/2)
		return term

	# end case




