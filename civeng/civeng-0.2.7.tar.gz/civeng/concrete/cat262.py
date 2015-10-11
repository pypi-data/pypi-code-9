
from math import sqrt
from .params import beton_dict, betonstahl_dict, es
from ..results import Results

code = 'SIA 262:13'


def index(name):
	data = {
		
	}
	return data.get(name, '')


def kt(w, h):
	""" (99) kt [-]"""
	kt = 1/(1+0.5*t(w, h))
	return kt


def t(w, h):
	""" () t [m] """
	# jeweils kleinste Abmessung massgebend
	# term = min(b, h)
	# für Platten- und Rechteckquerschnitte
	term = h/3 * 1e-3  # t in m
	return term


class Beton(Results):
	code = code
	
	def __init__(self, choice, gamma_c, eta_t=1.0):
		key = list(beton_dict)[choice]
		self.fck, self.fctm, self.beta_fc = beton_dict[key]
		self.gamma_c = gamma_c
		self.eta_t_ = eta_t

	def fck_(self):
		print('fck from cat262: {}'.format(self.fck))
		return self.fck

	def fcd(self):
		""" (2) """
		term = self.eta_fc()*self.eta_t()*self.fck/self.gamma_c
		term = round(term*2)/2
		self.add_rslt('fcd', term, 'f.cd', 'N/mm^2', '2.3.2.3', 2)
		return term

	def eta_fc(self):
		""" (26) """
		term = (30/self.fck)**(1/3)
		term = 1.0 if term >= 1.0 else term
		self.add_rslt('eta_fc', term, '&eta;.fc', '-', '4.2.1.2', 26)
		return term

	def eta_t(self):
		""" (27) """
		if isinstance(self.eta_t_, tuple):
			fcm_tL, fcm_tP = self.eta_t_
			term = 0.85*fcm_tL/fcm_tP
			term = 1.0 if term >= 1.0 else term
		else:
			term = self.eta_t_
		self.add_rslt('eta_t', term, '&eta;.t', '-', '4.2.1.3', 27)
		return term

	def tau_cd(self):
		""" (3) """
		term = 0.3*self.eta_t()*sqrt(self.fck)/self.gamma_c
		term = round(term*2, 1)/2
		self.add_rslt('tau_cd', term, '&tau;.cd', '-', '2.3.2.4', 3)
		return term

	def fctd(self, w, h):
		""" (98) """
		term = kt(w, h)*self.fctm
		self.add_rslt('fctd', round(term, 1), 'f.ctd', 'N/mm^2', '4.4.1.3', 98)
		return term
	



class Betonstahl(Results):
	code = code
	
	def __init__(self, choice, gamma_s):
		key = list(betonstahl_dict)[choice]
		self.fsk, self.ks, self.epsilon_ud = betonstahl_dict[key]
		self.gamma_s = gamma_s

	def epsilon_yd(self):
		return self.fsd()/es

	def fsd(self):
		""" (4) fsd [N/mm2] """
		term = self.fsk/self.gamma_s
		term = round(term)
		self.add_rslt('fsd', term, 'f.sd', 'N/mm^2', '2.3.2.5', 4)
		return term

	def epsilon_v_el(self, md, mrd):
		"""" (38) """
		term = (self.fsd()/es)*(md/mrd)
		self.add_rslt('epsilon_v_el', round(term, 4), '\u03B5.v,el', '-', '4.3.3.2.2', '38')
		return term

	def epsilon_v_pl(self):
		""" (39) """
		term = 1.5*self.fsd()/es
		self.add_rslt('epsilon_v_pl', round(term, 4), '\u03B5.v,pl', '-', '4.3.3.2.2', '39')
		return term


class Cat262(Results):
	code = code

	def __init__(self):
		pass

	# 4.3.3 Shear Force
	
	# 4.3.3.2 Shear Force without Reinforcement

	def vrd(self, kd, tau_cd, d_v):
		""" (35) """
		term = kd*tau_cd*d_v
		self.add_rslt('vrd', round(term, 1), 'v.Rd', 'N/mm', '4.3.3.2.1', 35)
		return term

	def kd(self, epsilon_v, d, kg):
		""" (36) """
		term = 1/(1+epsilon_v*d*kg)
		self.add_rslt('kd', round(term, 2), 'k.d', '-', '4.3.3.2.1', 36)
		return term

	def kg(self, dmax):
		""" (37) """
		term = 48/(16+dmax)
		self.add_rslt('kg', round(term, 2), 'k.g', '-', '4.4.4.2.1', 37)
		return term


	
