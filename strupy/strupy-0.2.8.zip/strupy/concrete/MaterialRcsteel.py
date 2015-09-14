'''
--------------------------------------------------------------------------
Copyright (C) 2015 Lukasz Laba <lukaszlab@o2.pl>

File version 0.1 date 2015-06-30

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

class MaterialRcsteel :

    def __init__(self):
        print "MaterialRcsteel init"
        self.rcsteelname = 'B500'
        self.fyd = 420*u.MPa
        self.ksiefflim = 0.5

    def get_rcsteelinfo(self):
        return {"rcsteelname":self.rcsteelname, "fyd":self.fyd, "ksiefflim":self.ksiefflim}

    def set_rcsteelclass(self, newsteel):
        SteelTypes=[]
        SteelTypes.append({"rcsteelname":'B400', "fyd":350*u.MPa, "ksiefflim":0.53})
        SteelTypes.append({"rcsteelname":'B450', "fyd":375*u.MPa, "ksiefflim":0.53})
        SteelTypes.append({"rcsteelname":'B500', "fyd":420*u.MPa, "ksiefflim":0.5})
        for i in xrange(len(SteelTypes)):
            if newsteel==SteelTypes[i]['rcsteelname']:
                self.rcsteelname = SteelTypes[i]['rcsteelname']
                self.fyd = SteelTypes[i]['fyd']
                self.ksiefflim = SteelTypes[i]['ksiefflim']

# Test if main
if __name__ == '__main__':
    
    print ('test MaterialRcsteell')
    
    a=MaterialRcsteel()
    print a.get_rcsteelinfo()
    a.set_rcsteelclass('B450')
    print a.get_rcsteelinfo()
    a.set_rcsteelclass('B400')
    print a.get_rcsteelinfo()