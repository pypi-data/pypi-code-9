class DateIterator(object):

	CHRONOLOGICAL = 1
	STATIONARY = 0
	REVERSE_CHRONOLOGICAL = -1

	def __init__(self, start, end, increment_by_days=1):

		self.start = start
		self.end = end
		self.increment = increment_by_days 

		# what direction is this iterator moving in?
		if self.increment > 0:
			self.direction = self.CHRONOLOGICAL
		elif self.increment < 0:
			self.direction = self.REVERSE_CHRONOLOGICAL
		elif self.increment == 0:
			self.direction = self.STATIONARY

		# this is the difference between the first day and last day
		# within one date increment.  It is correctly 0 if increment
		# is either -1, 0, or 1.  
		# Generally 1 less than increment in magnitude
		self.span = self.direction * (abs(increment_by_days) - 1)

		# make sure that increment will move from start towards end
		if self.start > self.end and self.direction >= 0:
			raise ValueError(
				'If start date is after end date, the '
				'increment parameter should be positive.'
			)
		elif self.start < self.end and self.direction <=0:
			raise ValueError(
				'If start date is before end date, the '
				'increment parameter should be negative.'
			)

		self.pointer = start

	def __iter__(self):
		return self.__class__(self.start, self.end, self.increment)

	def next(self):
		if self.pointer > self.end and self.direction >= 0:
			raise StopIteration
		elif self.pointer < self.end and self.direction <= 0:
			raise StopIteration

		interval_start = self.pointer
		interval_end = self.pointer + timedelta(self.span)

		# If interval end falls outside the range, use the range's endpoint
		if interval_end > self.end and self.direction >= 0:
			interval_end = self.end
		elif interval_end < self.end and self.direction <= 0:
			interval_end = self.end

		self.pointer += timedelta(self.increment)

		return interval_start, interval_end
