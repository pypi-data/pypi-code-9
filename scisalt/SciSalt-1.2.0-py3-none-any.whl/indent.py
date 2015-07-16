from __future__ import print_function
import numpy as _np

class Indent(object):
	def __init__(self,level=0,basestr='\t'):
		self._level   = level
		self.basestr = basestr

	def _get_level(self):
		return _np.int64(self._level)
	def _set_level(self,value):
		self._level = _np.int64(value)
		if self._level < 0:
			warnings.warn('Can''t set indent level below zero. Setting to zero.',RuntimeWarning,stacklevel=2)
			self._level = _np.int64(0)
	level = property(_get_level,_set_level)

	def string(self):
		return self.basestr*self.level

def iprint(indent,*args,**kwargs):
	if len(args) >0:
		if type(args[0]) in [str, unicode]:
			newargs = ('{}{}'.format(indent.string(),args[0]),) + args[1:]
			print(*newargs,**kwargs)

def vprint(indent,verbose=False,*args,**kwargs):
	if verbose:
		iprint(indent,*args,**kwargs)
