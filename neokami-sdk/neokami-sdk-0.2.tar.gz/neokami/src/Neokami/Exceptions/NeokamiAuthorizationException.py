''' Copyright 2015 Neokami GmbH. '''

from .NeokamiBaseException import NeokamiBaseException

class NeokamiAuthorizationException(NeokamiBaseException):
	'''raise this when there's a Auth error'''