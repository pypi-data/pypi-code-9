
from inspect import getdoc
from math import sqrt
from .params import beton_dict, betonstahl_dict
from ..results import Results


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
	standard = 'SIA 262:13'
	
	def __init__(self, choice, gamma_c, eta_t=1.0):
		Results.__init__(self)
		key = list(beton_dict)[choice]
		self.fck, self.fctm, self.beta_fc = beton_dict[key]
		self.gamma_c = gamma_c
		self.eta_t_ = eta_t

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
	standard = 'SIA 262:13'
	
	def __init__(self, choice, gamma_s):
		Results.__init__(self)
		key = list(betonstahl_dict)[choice]
		self.fsk, self.ks, self.epsilon_ud = betonstahl_dict[key]
		self.gamma_s = gamma_s
		
	def fsd(self):
		""" (4) fsd [N/mm2] """
		term = self.fsk/self.gamma_s
		term = round(term)
		self.add_rslt('fsd', term, 'f.sd', 'N/mm^2', '2.3.2.5', 4)
		return term

