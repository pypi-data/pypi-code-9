"""
Demonstration code used in, or while writing, the documentation.
"""

from options import Options, attrs, Unset

class ClassicShape(object):
    
    name   = 'Shapes Rule!'
    color  = 'purple'
    height = 50
    width  = 50

    def __init__(self, name=None, color='white', height=10, width=10):
        self.name   = name
        self.color  = color
        self.height = height
        self.width  = width
    
    def draw(self, **kwargs):
        name   = kwargs.get('name',   self.name)
        color  = kwargs.get('color',  self.color)
        height = kwargs.get('height', self.height)
        width  = kwargs.get('width',  self.width)
        print "color='{}', width={}, name='{}', height={}".format(color, width, name, height)
        
    def draw2(self, name=None, color=None, height=None, width=None):
        name   = name   or self.name
        color  = color  or self.color
        height = height or self.height
        width  = width  or self.width
        print "color='{}', width={}, name='{}', height={}".format(color, width, name, height)
        
    def draw3(self, name=None, color=None, height=None, width=None):
        name   = name   or self.name   or ClassicShape.name
        color  = color  or self.color  or ClassicShape.color
        height = height or self.height or ClassicShape.height
        width  = width  or self.width  or ClassicShape.width
        print "color='{}', width={}, name='{}', height={}".format(color, width, name, height)
        
oldone = ClassicShape(name='one')
oldone.draw()
oldone.draw(color='red')
oldone.draw(color='green', width=22)

print "--"
oldone.draw2()
oldone.draw2(color='red')
oldone.draw2(color='green', width=22)

print "--"
oldone.draw3()
oldone.draw3(color='red')
oldone.draw3(color='green', width=22)

print '==='



def relative_meta(key):
    def setter(v, current):
        return int(v) + current[key] if isinstance(v, str) else v
    return setter

def relative(value, currently):
    return int(value) + currently if isinstance(value, str) else value

def relmath(value, currently):
    if isinstance(value, str):
        if value.startswith('*'):
            return currently * int(value[1:])
        elif value.startswith('/'):
            return currently / int(value[1:])
        else:
            return currently + int(value)
    else:
        return value
    
class Shape(object):

    options = Options(
        name   = None,
        color  = 'white',
        height = 10,
        width  = 10,
    )
    
    options.magic(
        height = lambda v, cur: cur.height + int(v) if isinstance(v, str) else v,
        width  = lambda v, cur: cur.height + int(v) + cur.width  if isinstance(v, str) else v,
    )
    
    options.magic(
        height = lambda v, cur: relmath(v, cur.height),
        width  = lambda v, cur: relmath(v, cur.width)
    )
  
    
    def __init__(self, **kwargs):
        self.options = Shape.options.push(kwargs)
    
    def _attrs(self, opts):
        nicekeys = [ k for k in opts.keys() if not k.startswith('_') ]
        return ', '.join([ "{}={}".format(k, repr(opts[k])) for k in nicekeys ])

    def draw(self, **kwargs):
        opts = self.options.push(kwargs)
        print attrs(opts)
        
    def draw2(self, **kwargs):
        opts = self.options.push(kwargs)
        print self._attrs(opts)
        
    def set(self, **kwargs):
        self.options.set(**kwargs)
        
    def is_tall(self, **kwargs):
        opts = self.options.push(kwargs)
        return opts.height > 100
    
    @options.magical('name')
    def capitalize_name(self, v, cur):
        return ' '.join(w.capitalize() for w in v.split())

one = Shape(name='one')
one.draw()
one.draw(color='red')
one.draw(color='green', width=22)

print '--'
Shape.options.set(color='blue')
one.draw()
one.draw(height=100)
one.draw(height=44, color='yellow')

print '---'
one.draw(width='+200')
one.draw()

print '----'
one.draw(width='*4', height='/2')
one.draw2(width='*4', height='/2')

print '-----'
one.set(width='*10', color='orange')
one.draw()
one.set(color=Unset)
one.draw()

print "------"
one.set(name='a shape')
one.draw()