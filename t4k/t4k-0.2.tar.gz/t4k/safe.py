def _filter_min_max_args(*args):

	if len(args) == 1:
		args = args[0]

	# filter out arguments that are None
	try:
		filtered_args = [i for i in args if i is not None]

	# arguments not iterable (i.e. a single non-iterable value was passed)
	except TypeError:
		if args is None:
			return None
		else:
			filtered_args = args

	# if argument was iterable, but is empty after filtering, return None
	else:
		if len(filtered_args) == 0:
			return None

	return filtered_args


def safe_max(*args):

	# filter out None's
	args = _filter_min_max_args(*args)
	if args is None:
		return None

	# delegate to max
	return max(*args)


def safe_min(*args):

	# filter out None's
	args = _filter_min_max_args(*args)
	if args is None:
		return None

	# delegate to min
	return min(*args)


def safe_lte(val1, val2):
	if val1 is None:
		return False
	if val2 is None:
		return True
	return val1 <= val2

def safe_lt(val1, val2):
	if val1 is None:
		return False
	if val2 is None:
		return True
	return val1 < val2

def safe_gte(val1, val2):
	if val1 is None:
		return False
	if val2 is None:
		return True
	return val1 >= val2

def safe_gt(val1, val2):
	if val1 is None:
		return False
	if val2 is None:
		return True
	return val1 > val2
