from collections import OrderedDict

class LinguisticVar:
    def __init__(self, name, minval=-10, maxval=10):
        self._name = name
        self._minval = minval
        self._maxval = maxval
        self._sets = OrderedDict()
        
    def get_name(self):
        return self._name
        
    def add_set(self, name, function):
        self._sets[name] = function
        
    def get_set(self, name):
        return self._sets[name]
        
    def get_range(self):
        return (self._minval, self._maxval)
        
    def set_range(self, minval, maxval):
        self._minval = minval
        self._maxval = maxval
        
