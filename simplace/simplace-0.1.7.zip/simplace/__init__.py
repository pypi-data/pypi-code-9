from .simplace import *
from ._version import __version__, __version_info__
__all__ = ['initSimplace', 'openProject','closeProject','runProject','setProjectLines',
            'createSimulation', 'runSimulation', 'setSimulationValues', 'stepSimulation',
			'setSimulationIDs', 'getResult', 'resultToList', 'varmapToList',
			'setLogLevel', 'setSlotCount', 'setCheckLevel'
]
