''' Copyright 2015 Neokami GmbH. '''

from .NeokamiBaseException import NeokamiBaseException

class NeokamiSDKException(NeokamiBaseException):
	'''raise this when there's a SDK error'''