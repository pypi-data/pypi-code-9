class Mash(object):	
	def __init__(self, data={}):
		data = {k:(Mash(v) if isinstance(v, dict) else v) for k,v in data.items()}
		super(Mash, self).__setattr__('_dict_instance', data)

	def __getattr__(self, name):
		return self._dict_instance[name]

	def __getitem__(self, name):
		return self._dict_instance[name]

	def __setattr__(self, name, value):
		self._dict_instance[name] = value

	def __setitem__(self, name, value):
		self._dict_instance[name] = value

	def __contains__(self, item):
		return item in self._dict_instance

	def __str__(self):
		return 'Mash:' + self._dict_instance.__str__()

	def __repr__(self):
		return 'mash(' + self._dict_instance.__repr__() + ')'