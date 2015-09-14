'''
--------------------------------------------------------------------------
Copyright (C) 2015 Lukasz Laba <lukaszlab@o2.pl>

File version 0.1 date 2015-07-01

This file is part of StruPy.
StruPy is a structural engineering design Python package.
http://strupy.org/

StruPy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import strupy.units as u

class MaterialConcrete :
    
    def __init__(self):
        print "Material_concrete init"
        self.concretename = 'C25/30'
        self.fcd = 16.7*u.MPa
        self.fctm = 2.6*u.MPa

    def get_concreteinfo(self):
        return {"concretename":self.concretename, "fcd":self.fcd, "fctm":self.fctm}

    def set_concreteclass(self, newconcrete):
        ConcreteTypes=[]
        ConcreteTypes.append({"concretename":'C12/15', "fcd":8.0*u.MPa, "fctm":1.6*u.MPa})
        ConcreteTypes.append({"concretename":'C16/20', "fcd":10.6*u.MPa, "fctm":1.9*u.MPa})
        ConcreteTypes.append({"concretename":'C20/25', "fcd":13.3*u.MPa, "fctm":2.2*u.MPa})
        ConcreteTypes.append({"concretename":'C25/30', "fcd":16.7*u.MPa, "fctm":2.6*u.MPa})
        ConcreteTypes.append({"concretename":'C30/37', "fcd":20.0*u.MPa, "fctm":2.9*u.MPa})
        ConcreteTypes.append({"concretename":'C35/45', "fcd":23.3*u.MPa, "fctm":3.2*u.MPa})
        ConcreteTypes.append({"concretename":'C40/50', "fcd":26.7*u.MPa, "fctm":3.5*u.MPa})
        ConcreteTypes.append({"concretename":'C45/55', "fcd":30.0*u.MPa, "fctm":3.8*u.MPa})
        ConcreteTypes.append({"concretename":'C50/60', "fcd":33.3*u.MPa, "fctm":4.1*u.MPa})
        for i in xrange(len(ConcreteTypes)):
            if newconcrete==ConcreteTypes[i]['concretename']:
                self.concretename = ConcreteTypes[i]['concretename']
                self.fcd = ConcreteTypes[i]['fcd']
                self.fctm = ConcreteTypes[i]['fctm']

# Test if main
if __name__ == '__main__':
    print ('test MaterialConcrete')
    a=MaterialConcrete()
    print a.get_concreteinfo()
    print a.set_concreteclass("C12/15")
    print a.get_concreteinfo()
    print a.set_concreteclass("C16/205")
    print a.get_concreteinfo()
    print a.set_concreteclass("C20/25")
    print a.get_concreteinfo()
    print a.set_concreteclass("C30/37")
    print a.get_concreteinfo()
    print a.set_concreteclass("C35/45")
    print a.get_concreteinfo()
    print a.set_concreteclass("C40/50")
    print a.get_concreteinfo()
    print a.set_concreteclass("C45/55")
    print a.get_concreteinfo()
    print a.set_concreteclass("C50/60")
    print a.get_concreteinfo()