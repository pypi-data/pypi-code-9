from stuf import stuf
class A(object):
    def __init__(self):
        self.s = stuf()

    def __getattr__(self, key):
        # handle normal object attributes
        if key in self.__dict__:
            return self.__dict__[key]
        # handle special attributes
        else:
            return self.s[key]
    
    def __setattr__(self, key, value):
        # handle normal object attributes
        if key == 's' or key in self.__dict__:
            object.__setattr__(self, key, value)
        else:
            self.s[key] = value
            
    def magic(self, key, func):
        def fget(key):
            return self.s[key]
        def fset(key, value):
            self.s[key] = func(value)
        def fdel(key):
            del self.s[key]
        self.__dict__[key] = property(fget, fset, fdel, 'magic for {}'.format(key))
        print "setting magic"
        
    @property
    def slick(self):
        return self.s['slick']
    
    @slick.setter
    def slick(self, value):
        self.s['slick'] = 2 * value

class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value * 2

    @x.deleter
    def x(self):
        del self._x
        
class D(object):
    def __init__(self):
        self.s = stuf()

    @property
    def x(self):
        """I'm the 'x' property."""
        return self.s['x']
    
    @x.setter
    def x(self, value):
        self.s['x'] = value * 2

    @x.deleter
    def x(self):
        del self.s['x']
        
class E(object):
    def __init__(self):
        self.s = stuf()
        
    def magic(self, key, func):
        def fget(key):
            return self.s[key]
        def fset(key, value):
            self.s[key] = func(value)
        def fdel(key):
            del self.s[key]
        self.__class__.x = property(fget, fset, fdel, 'magic for {}'.format(key))
    
    # nb must set property in __class__ (here, E) not in instance (e)
    
class Setter(object):
    def __init__(self, initial, setter=None, getter=None):
        self.initial = initial
        self.setter = setter
        self.getter = getter
    
class Stuffer(object):
    def __init__(self, **kwargs):
        self.s = stuf()
        self.magic = dict()
        for k,v in kwargs.items():
            if isinstance(v, Setter):
                self.s[k] = v.initial
                self.magic[k] = v.setter
            else:
                self.s[k] = v

    def __getattr__(self, key):
        # handle normal object attributes
        if key in self.__dict__:
            return self.__dict__[key]
        # handle special attributes
        elif key in self.magic:
            getter = self.magic[key]
            return getter(self.s[key]) if getter else self.s[key]   
        else:
            return self.s[key]
    
    def __setattr__(self, key, value):
        # handle normal object attributes
        if key == 's' or key == 'magic' or key in self.__dict__:
            object.__setattr__(self, key, value)
        elif key in self.magic:
            value = self.magic[key](value)
            self.s[key] = value
        else:
            self.s[key] = value
            
class Stufer(stuf):
    def __init__(self, **kwargs):
        stuf.__init__(self)
        self._magic = dict()
        for k,v in kwargs.items():
            if isinstance(v, Setter):
                self[k] = v.initial
                self._magic[k] = v
            else:
                self[k] = v
                
    def __getattr__(self, key):
        # handle normal object attributes
        if key == '_magic' or key in self.__dict__:
            return self.__dict__[key]  # BREAKS HERE
        # handle special attributes
        elif key in self._magic:
            getter = self._magic[key].getter
            return getter(self[key]) if getter else self[key]   
        else:
            return self[key]
    
    def __setattr__(self, key, value):
        # handle normal object attributes
        if key == '_magic' or key in self.__dict__:
            stuf.__setattr__(self, key, value)
        elif key in self._magic:
            value = self._magic[key].setter(value)
            self[key] = value
        else:
            self[key] = value
            
if __name__ == '__main__':
    a = A()
    a.something = 144
    print a.something
    a.magic('woobers', lambda x: 2 * x)
    a.woobers = 10
    print a.woobers
    a.slick = 10
    print a.slick
    print "--"
    c = C()
    c.x = 12
    print c.x
    print "---"
    d = D()
    d.x = 5
    print d.x
    print "---"
    e = E()
    e.magic('x', lambda value: value * 2)
    e.x = 9
    print e.x
    print e.s
    print "==="
    s = Stuffer(this=1, that=2, name='joe')
    print s.name
    t = Stuffer(this=12, name=Setter('joe', lambda x: x.upper()))
    print t.name
    t.name = 'frank'
    print t.name
    print "===***"
    s = Stufer(this=1, that=2, name='joe')
    print s.name
    t = Stufer(this=12, name=Setter('joe', lambda x: x.upper()))
    print t.name
    t.name = 'frank'
    print t.name
  
# playing with options for property setting