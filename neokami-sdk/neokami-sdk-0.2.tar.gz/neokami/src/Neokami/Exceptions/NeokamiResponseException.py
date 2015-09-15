''' Copyright 2015 Neokami GmbH. '''

from .NeokamiBaseException import NeokamiBaseException

class NeokamiResponseException(NeokamiBaseException):
	'''raise this when there's a Response error'''