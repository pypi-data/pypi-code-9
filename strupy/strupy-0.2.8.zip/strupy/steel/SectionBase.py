'''
--------------------------------------------------------------------------
Copyright (C) 2015 Lukasz Laba <lukaszlab@o2.pl>

File version 0.1 date 2015-09-12

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
import xml.etree.ElementTree as ET
import copy
import os

import strupy.units as u

class SectionBase :
    
    def __init__(self):
        self.__database='sectionbase_EuropeanSectionDatabase.xml'
        self.__package_dir = os.path.split(__file__)[0]
        self.__xmlbase_path = os.path.join(self.__package_dir, "database_sections", self.__database)
        self.__tree = ET.parse(self.__xmlbase_path)
        self.__root = self.__tree.getroot()
        self.__sectiondictwithparam=self.__get_database_sectiondictwithparam()

    def __get_database_sectiondictwithparam(self):
        sectiondictwithpatam={}
        for item in self.__root.iter('sectionlist_item'):
            sectiondictwithpatam[item.attrib['sectionname']]=self.__sectionparameters_unitaplly(copy.deepcopy(item.attrib))
        for i in sectiondictwithpatam:
            sectiondictwithpatam[i]['Wy']=\
            sectiondictwithpatam[i]['Iy']/max(sectiondictwithpatam[i]['vz'],sectiondictwithpatam[i]['vpz']).normalize()
            sectiondictwithpatam[i]['Wz']=\
            sectiondictwithpatam[i]['Iz']/max(sectiondictwithpatam[i]['vy'],sectiondictwithpatam[i]['vpy']).normalize()
        return sectiondictwithpatam
        
    def get_database_name(self):
        name=[]
        for item in self.__root.iter('baseinformation'):
            name = item.attrib
        return name['basetitle']
        
    def get_database_sectiontypes(self):
        sectiontypes=[]
        for item in self.__root.iter('sectiontype_item'):
            sectiontypes.append(item.attrib ['figure'])
        return sectiontypes
        
    def get_database_sectiontypesdescription(self):
        description={}
        for item in self.__root.iter('sectiontype_item'):
            description[item.attrib ['figure']]=item.attrib ['description']
        return description
        
    def get_database_sectionlist(self):
        sectionlist=[]
        for item in self.__root.iter('sectionlist_item'):
            sectionlist.append(item.attrib ['sectionname'])
        return sectionlist
        
    def get_database_sectionlistwithtype(self, secttype='IPE'):
        sectionlistwithtype=[]
        for item in self.__root.iter('sectionlist_item'):
                if item.attrib['figure'] == secttype :
                    sectionlistwithtype.append(item.attrib ['sectionname'])
        return sectionlistwithtype

    def __sectionparameters_unitaplly(self, param):
        lu = u.m.asUnit(u.m)        #long_unit
        sdu = u.m.asUnit(u.cm)      #sectdim_unit
        wu = u.kg                   #weight_unit
        #---------------------------------
        param['mass']=float(param['mass'])*wu/lu
        param['surf']=float(param['surf'])*sdu**2/lu
        param['h']=float(param['h'])*sdu
        param['b']=float(param['b'])*sdu
        param['ea']=float(param['ea'])*sdu
        param['es']=float(param['es'])*sdu
        param['ra']=float(param['ra'])*sdu
        param['rs']=float(param['rs'])*sdu
        param['gap']=float(param['gap'])*sdu
        param['Ax']=float(param['Ax'])*sdu**2
        param['Ay']=float(param['Ay'])*sdu**2
        param['Az']=float(param['Az'])*sdu**2
        param['Ix']=float(param['Ix'])*sdu**4
        param['Iy']=float(param['Iy'])*sdu**4
        param['Iz']=float(param['Iz'])*sdu**4
        param['Iomega']=float(param['Iomega'])*sdu**4
        param['vy']=float(param['vy'])*sdu
        param['vpy']=float(param['vpy'])*sdu
        param['vz']=float(param['vz'])*sdu
        param['vpz']=float(param['vpz'])*sdu
        param['Wply']=float(param['Wply'])*sdu**3
        param['Wplz']=float(param['Wplz'])*sdu**3
        param['Wtors']=float(param['Wtors'])*sdu**3
        param['gamma']=float(param['gamma'])
        #---------------------------------
        return  param
        
    def get_sectionparameters(self, sectname='IPE 270'):
        return self.__sectiondictwithparam[sectname]
        
    def ui_get_sectionparameters(self):
        import Tkinter
        root=Tkinter.Tk()
        root.title('StrupySteelSectionBrowser')
        def cb_secname(e):
            global sectname
            sectname = L1.get(L1.curselection())
            t.delete(1.0,Tkinter.END)
            param_tmp=self.get_sectionparameters(sectname)
            for key in param_tmp:
                t.insert(Tkinter.END, key + '=' + str(param_tmp[key]) +'\n')
        def cb_secname_1(e):
            cb_secname
            root.quit()
            root.destroy()
        def cb_sectype(e):
            L1.delete(0,L1.size())
            for item in self.get_database_sectionlistwithtype(L.get(L.curselection())):
                L1.insert(Tkinter.END, item)
        s = Tkinter.Scrollbar()
        s1 = Tkinter.Scrollbar()
        L = Tkinter.Listbox()
        L1 = Tkinter.Listbox()
        t=Tkinter.Text()
        s.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        s1.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        L.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        L1.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        t.pack()
        L.bind('<<ListboxSelect>>', cb_sectype)
        L1.bind('<<ListboxSelect>>', cb_secname)
        L1.bind('<Double-Button-1>', cb_secname_1)
        s.config(command=L.yview)
        s1.config(command=L1.yview)
        L.config(yscrollcommand=s.set)
        L1.config(yscrollcommand=s1.set)
        for item in self.get_database_sectiontypes():
            L.insert(Tkinter.END, item)
        root.mainloop()
        return self.get_sectionparameters(sectname)

    def get_parameters_description(self):
        descriptiondir=[]
        for item in self.__root.iter('parameterdescription'):
            descriptiondir = item.attrib
        descriptiondir['Wy'] = 'Elastic section modulus about Y axis'
        descriptiondir['Wz'] = 'Elastic section modulus about Z axis'
        return descriptiondir
    
    def find_withparameter(self, parameter='mass', value=40*u.kg/u.m, delta_n=-0.2, delta_p=0.2):
        sectionlist=[]
        for i in self.__sectiondictwithparam.iterkeys():
            if value*(1+delta_n) < self.__sectiondictwithparam[i][parameter] < value*(1+delta_p):
                sectionlist.append(str(i))
        return sectionlist

# Test if main
if __name__ == '__main__':
    print ('test DataBaseBrowser')
    base=SectionBase()
    print('start')
    print base.get_database_name()
    print base.get_database_sectiontypes()
    print base.get_database_sectiontypesdescription()['IPEA']
    print base.get_database_sectionlist()
    print base.get_database_sectionlistwithtype('HEA')
    print base.get_sectionparameters("HE 200 B")
    print base.ui_get_sectionparameters()
    print base.get_parameters_description()
    print base.find_withparameter()

    
    
