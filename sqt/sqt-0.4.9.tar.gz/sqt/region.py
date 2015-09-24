"""
Model an interval on a reference.
"""
class Region:
	def __init__(self, specification):
		"""
		specification -- description of the region as a string
		"""
		self.reference, self.start, self.stop, self.is_reverse_complement = self._parse_region(specification)

	@staticmethod
	def _parse_region(s):
		"""
		Parse a string like "name:begin-end".
		The returned tuple is (name, start, stop, revcomp).
		start is begin-1, stop is equal to end.

		The string may be prefixed with "rc:", in which case revcomp is set to True.

		If 'end' is not given (as in "chrx:1-"), then stop is set to None.
		If only 'name' is given (or "rc:name"), start is set to 0 and stop to None.

		Commas within the numbers are ignored.

		This function converts from 1-based intervals to pythonic open intervals!
		"""
		revcomp = False
		if s.startswith('rc:'):
			revcomp = True
			s = s[3:]
		fields = s.rsplit(':', 1)
		if len(fields) == 1:
			region = (fields[0], 0, None, revcomp)
		else:
			start, stop = fields[1].split('-')
			start = int(start.replace(',', ''))
			stop = int(stop.replace(',', '')) if stop != '' else None
			assert 0 < start and (stop is None or start <= stop)
			region = (fields[0], start-1, stop, revcomp)
		return region

	def __str__(self):
		"""

		"""
		prefix = 'rc:' if self.is_reverse_complement else ''
		if self.start == 0 and self.stop is None:
			return prefix + self.reference
		stop = '' if self.stop is None else self.stop
		return "{}{}:{}-{}".format(prefix, self.reference, self.start+1, stop)

	def __repr__(self):
		return "Region({!r})".format(str(self))
