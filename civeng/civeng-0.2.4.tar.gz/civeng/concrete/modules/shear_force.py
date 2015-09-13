
from math import sin, cos, radians
from .bending_force import BendingForce
from ..cat262 import Beton, Betonstahl, Cat262
from ..params import dm_set, epsilon_c2d, epsilon_ud
from ...funcs import as_
from ...results import Results


class ShearForceWithoutReinfrocement(Results):
	code = 'SIA 262:13'
	selection = ['vrd']

	def __init__(self, entries):

		self.mrd = BendingForce(entries).mrd()
		self.concrete = Beton(entries['beton'], entries['gamma_c'])
		self.betonstahl = Betonstahl(entries['betonstahl'], entries['gamma_s'])
		self.cat262 = Cat262()

		dm_inf = dm_set[entries['dm_inf']]
		s_inf = entries['s_inf']
		self.as_inf = as_(dm_inf, s_inf)
		self.d_inf = int(entries['d_inf'])

		self.w = int(entries['w'])
		self.h = int(entries['h'])

		self.dm_a = entries['dm_a']
		self.md = entries['md']*1e6

		self.concrete_type = 'normal'
		self.state = entries['state']
		self.dmax = entries['dmax']
		self.ff43323 = entries['ff43323']
		self.ff43324 = entries['ff43324']
		self.theta = entries['theta']

	def compute(self):
		self.vrd()
		return  self.get_results()

	def vrd(self):
		if self.dm_a > self.d_inf/6:
			dv = self.d_inf-self.dm_a
		else:
			dv = self.d_inf
		term = self.cat262.vrd(self.kd(), self.concrete.tau_cd(), dv)
		return term

	def kd(self):
		if self.state == 'elastic':
			if self.md == 0:
				md, mrd = 1, 1
			else:
				md, mrd = self.md, self.mrd
			epsilon_v = self.betonstahl.epsilon_v_el(md, mrd)
		else:
			epsilon_v = self.betonstahl.epsilon_v_pl()
		if self.ff43323:
			epsilon_v *= 1.5
		if self.ff43324:
			theta = radians(self.theta)
			epsilon_v *= 1/(sin(theta)**4+cos(theta)**4)
		term = self.cat262.kd(epsilon_v, self.d_inf, self.kg())
		return term

	def kg(self):
		if self.concrete_type != 'normal' or self.concrete.fck > 70:
			self.dmax = 0
		term = self.cat262.kg(self.dmax)
		return term



