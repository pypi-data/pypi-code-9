''' Copyright 2015 Neokami GmbH. '''

from .NeokamiBaseException import NeokamiBaseException

class NeokamiBlockedException(NeokamiBaseException):
	'''raise this when there's a Blocked error'''
