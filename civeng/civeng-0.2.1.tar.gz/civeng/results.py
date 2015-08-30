




def descr(name):
	
	descr = {
		'eta_fc': 'Umrechnungsfaktor',
		'eta_t': 'Umrechnungsfaktor für Betonfestigkeiten',
		'fcd': 'Bemessungswert der Druckfestigkeit',
		'fctd': 'Bemessungswert der Betonzugfestigkeit',
		'fsd': 'Bemessungswert der Fliessgrenze von Betonstahl',
		'mrd': 'Widerstandsmoment',
		'mrd_': 'Rissmoment',
	}
	
	return descr.get(name, '')





def sort_results(rslts):
	return [rslts[k] for k in sorted(rslts)]



class Results:
	
	def __init__(self):
		self.main_rslts = {}
		self.semi_rslts = {}
		self.resultsf = {}
	
	def add_rslt(self, name, rslt, lbl, unit, ff='', f=''):
		self.resultsf[name] = {
			'name': name,
			'standard': self.standard,
			'ff': '{} {}'.format(self.standard, ff),
			'f': f,
			'description': descr(name),
			'label': lbl,
			'result': rslt,
			'unit': unit,
			}
		

	
	def get_results(self):
		return self.resultsf
	
	def get_semi_rslts(self):
		return sort_results(self.semi_rslts)
	
	
	def sorted_results(self):
		return [self.resultsf[k] for k in sorted(self.resultsf)]
	
	def quick_results(self, pick):
		return [self.resultsf[k] for k in pick]