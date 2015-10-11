
import inspect

def descr(name):
	
	descr = {
		'as_max_stat_d': 'Max. Bewehrung für stat. best. Sys.',
		'as_max_stat_ind': 'Max. Bewehrung für stat. unbest. Sys.',
		'as_min': 'Mindestbewehrung',
		'epsilon_s_inf': 'Stahldehnung unten',
		'epsilon_v_el': 'Dehnung im elastischen Zustand',
		'eta_fc': 'Umrechnungsfaktor zur Berücksichtigung des Bruchverhaltens',
		'eta_t': 'Umrechnungsfaktor für Betonfestigkeiten',
		'fcd': 'Bemessungswert der Betondruckfestigkeit',
		'fctd': 'Bemessungswert der Betonzugfestigkeit',
		'fsd': 'Bemessungswert der Fliessgrenze Betonstahl',
		'kd': 'Beiwert zur Bestimmung des Querkraftwiderstands',
		'kg': 'Beiwert zur Berücksichtigung des Grösstkorns',
		'mrd': 'Widerstandsmoment',
		'mrd_': 'Rissmoment',
		'mrd_max_stat_d': 'Max. Widerstandsm. für stat. best. Sys.',
		'mrd_max_stat_ind': 'Max. Widerstandsm. für stat. unbest. Sys.',
		'tau_cd' : 'Bemessungswert der Schubspannungsgrenze',
		'vrd': 'Bemessungswert des Querkraftwiderstands',
		'x': 'Druckzonenhöhe',
		'z': 'Innerer Hebelarm',
	}

	return descr.get(name, '')


def descr2(name):
	
	descr = {
		'epsilon_s_inf': ('', '', '\u03B5.s,inf', '\u2030', 'Stahldehnung unten'),
	}
	return descr.get(name, '')



class Results:
	resultsf = {}
	messages = {}

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


	def add_rslt2(self, result, reference=''):
		name = inspect.stack()[1][3]
		ff, f, label, unit, description = descr2(name)
		self.resultsf[name] = {
			'name': name,
			'standard': self.code,
			'ff': '{} {}'.format(self.code, ff),
			'f': f,
			'description': description,
			'label': label,
			'result': result,
			'unit': unit,
		}
		if reference and result > reference:
			comparison = '{} > {}'.format(result, reference)
			self.resultsf[name].update({'result': comparison})
			self.messages[name] = {'name': name}


	def add_msg(self, name, msg):
		self.messages[name] = msg
		

	def sorted_results(self):
		return [self.resultsf[k] for k in sorted(self.resultsf)]

	def quick_results(self):
		return [self.resultsf[k] for k in self.selection]
	
	def get_results(self):
		print('messages: {}'.format(self.messages))
		results = {'main_rslts': self.sorted_results(), 
				'quick_rslts': self.quick_results(),
				'messages': self.messages.copy()}
		self.resultsf.clear()
		self.messages.clear()
		return results
	



