def create_group(level,name):
	try:
		level.create_group(name)
	except ValueError as e:
		if e.message != 'Unable to create group (Name already exists)':
			raise
