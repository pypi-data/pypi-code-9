#from .utils import (json_read,
                    #json_write)


#class Option(object):
    #def __init__(self, name, default=None, opt_type=None):
        #self.name = name
        #self.default = default
        #self.opt_type = opt_type

        #if opt_type is not None and default is not None and not isinstance(default, self.opt_type):
            #self.default = self.opt_type(default)

    #def __get__(self, obj, type=None):
        #pass

    #def __set__(self, obj, value):
        #raise AttributeError


##class MetaConfig(type):

    ##def __new__(mcs, name, bases, attrs):
        ##metaOptions = attrs.pop('MetaOptions', None)
        ##cls = super(MetaConfig, mcs).__new__(name, bases, attrs)
        ##if metaOptions is not None:
            ##for name, val in metaOptions.__dict__.items():
                ##if isinstance(val, Option):
                    ##cls.setattr(name)



#class Config(object):
    ##class MetaOptions:
        ##pass
    #def __init__(self, file_path):
        #self.file_path = file_path
        #self._config = json_read(file_path)

    #def
