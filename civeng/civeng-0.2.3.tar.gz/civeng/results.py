


def descr(name):
	
	descr = {
		'as_max_stat_d': 'Max. Bewehrung für stat. best. Sys.',
		'as_max_stat_ind': 'Max. Bewehrung für stat. unbest. Sys.',
		'as_min': 'Mindestbewehrung',
		'epsilon_s_inf': 'Stahldehnung unten',
		'eta_fc': 'Umrechnungsfaktor',
		'eta_t': 'Umrechnungsfaktor für Betonfestigkeiten',
		'fcd': 'Bemessungswert der Betondruckfestigkeit',
		'fctd': 'Bemessungswert der Betonzugfestigkeit',
		'fsd': 'Bemessungswert der Fliessgrenze Betonstahl',
		'mrd': 'Widerstandsmoment',
		'mrd_': 'Rissmoment',
		'mrd_max_stat_d': 'Max. Widerstandsm. für stat. best. Sys.',
		'mrd_max_stat_ind': 'Max. Widerstandsm. für stat. unbest. Sys.',
		'x': 'Druckzonenhöhe',
		'z': 'Innerer Hebelarm',
	}

	return descr.get(name, '')




class Results:
	resultsf = {}

	def __init__(self):
		pass

	def add_rslt(self, name, rslt, lbl, unit, ff='', f=''):
		self.resultsf[name] = {
			'name': name,
			'standard': self.code,
			'ff': '{} {}'.format(self.code, ff),
			'f': f,
			'description': descr(name),
			'label': lbl,
			'result': rslt,
			'unit': unit,
			}
		
	def sorted_results(self):
		return [self.resultsf[k] for k in sorted(self.resultsf)]

	def quick_results(self):
		return [self.resultsf[k] for k in self.selection]
	
	def get_results(self):
		return {'main_rslts': self.sorted_results(), 'quick_rslts': self.quick_results()}
	



