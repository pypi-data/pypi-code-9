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

from RcRecSect import RcRecSect
from SectLoad import SectLoad

import math

class RcRecSectSolver():

    import fas as fas

    def __init__(self):
        print "RcRecSecSolver"
     
    def paraminfo(self):
        self.fas.paraminfo()

    def reinforce(self, sect, load):
        sect.An=0*u.m2
        sect.Ap=0*u.m2
        sect.comment=''
        casecalculated=[]
        caseAn=None
        caseAp=None
        for i in xrange(0, len(load.caseactiv)):
            if load.caseactiv[i]:
                tmp=self.fas.calc(load.Nsd[i], load.Msd[i], sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
                if sect.An<tmp['An']:
                    sect.An=tmp['An']
                    caseAn=i
                if sect.Ap<tmp['Ap']:
                    sect.Ap=tmp['Ap']
                    caseAp=i
                casecalculated.append(i)
        sect.comment+='case calculated - '+ str(casecalculated)+' case for Ap -'+ str(caseAp)+' case for An -'+ str(caseAn)
        return sect
        
    def resist_moment(self, sect, acompNsd=0*u.kN): 
        failurecode=None
        precision=5.78*u.kNm
        deltainit=200*u.kNm
        Mrdmax=0*u.kNm
        Apreq=0*u.m2
        Anreq=0*u.m2
        delta=deltainit
        alpha=1.0
        while abs(delta)>precision:
            Mrdmax=Mrdmax+delta*alpha
            tmp=self.fas.calc(acompNsd, Mrdmax, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
            Apreq=tmp['Ap']
            Anreq=tmp['An']
            if Apreq<=sect.Ap and Anreq<=sect.An:
                nextalpha=1.0
            else:
                nextalpha=-1.0
            if Mrdmax<0*u.kNm:
                Mrdmax=0*u.kNm
                nextalpha=-alpha
            if nextalpha*alpha==-1.0 :
                delta = 0.5*delta
            alpha=nextalpha
        Mrdmin=0*u.kNm
        Apreq=0*u.m2
        Anreq=0*u.m2
        delta=-deltainit
        alpha=1.0
        while abs(delta)>precision:
            print delta
            print Mrdmin
            Mrdmin=Mrdmin+delta*alpha
            tmp=self.fas.calc(acompNsd, Mrdmin, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
            Apreq=tmp['Ap']
            Anreq=tmp['An']
            if Apreq<=sect.Ap and Anreq<=sect.An:
                nextalpha=1.0
            else:
                nextalpha=-1.0
            if Mrdmin>0*u.kNm:
                Mrdmin=0*u.kNm
                nextalpha=-alpha
            if nextalpha*alpha==-1.0 :
                delta = 0.5*delta
            alpha=nextalpha
        #print {'Mrdmax':Mrdmax, 'Mrdmin':Mrdmin, 'acompNsd':acompNsd, 'failurecode':failurecode}
        sect.resist_moment={'Mrdmax':Mrdmax, 'Mrdmin':Mrdmin, 'acompNsd':acompNsd, 'failurecode':failurecode}
        return sect

    def resist_force(self, sect, acompMsd=0*u.Nm):
        failurecode=None
        precision=13.0*u.kN
        deltainit=600*u.kN
        Nrdmax=0*u.kN
        Apreq=0*u.m2
        Anreq=0*u.m2
        delta=deltainit
        alpha=1.0
        while abs(delta)>precision:
            print delta
            print Nrdmax
            Nrdmax=Nrdmax+delta*alpha
            tmp=self.fas.calc(Nrdmax, acompMsd, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
            Apreq=tmp['Ap']
            Anreq=tmp['An']
            if Apreq<=sect.Ap and Anreq<=sect.An:
                nextalpha=1.0
            else:
                nextalpha=-1.0
            if Nrdmax<0*u.kN:
                Nrdmax=0*u.kN
                nextalpha=-alpha
            if nextalpha*alpha==-1.0 :
                delta = 0.5*delta
            alpha=nextalpha
        Nrdmin=0*u.kN
        Apreq=0*u.m2
        Anreq=0*u.m2
        delta=-deltainit
        alpha=1.0
        while abs(delta)>precision:
            print delta
            print Nrdmin
            Nrdmin=Nrdmin+delta*alpha
            tmp=self.fas.calc(Nrdmin, acompMsd, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
            Apreq=tmp['Ap']
            Anreq=tmp['An']
            if Apreq<=sect.Ap and Anreq<=sect.An:
                nextalpha=1.0
            else:
                nextalpha=-1.0
            if Nrdmin>0*u.kN:
                Nrdmin=0*u.kN
                nextalpha=-alpha
            if nextalpha*alpha==-1.0 :
                delta = 0.5*delta
            alpha=nextalpha  
        #print {'Nrdmax':Nrdmax, 'Nrdmin':Nrdmin, 'acompMsd':acompMsd, 'failurecode':failurecode}
        sect.resist_force={'Nrdmax':Nrdmax, 'Nrdmin':Nrdmin, 'acompMsd':acompMsd, 'failurecode':failurecode}
        return sect

    def resist_forcetomoment(self, sect, dividenumber=10):
        Nrdi=[]
        Mrdi=[]
        Nrdi_withcrackcontrol=[]
        Mrdi_withcrackcontrol=[]
        failurecode=[]
        precisionN=13.0*u.kN
        precisionM=1.0*u.kNm
        deltainitN=1000*u.kN
        deltainitM=1000*u.kNm
        for i in xrange (0, dividenumber+1):
            beta=(2.0*math.pi)*i/dividenumber
            dNsdi=math.cos(beta)*deltainitN
            dMsdi=math.sin(beta)*deltainitM
            alpha=1.0
            Apreqi=0*u.m2
            Anreqi=0*u.m2
            n=0
            if True:
                Nsdi=0*u.kN
                Msdi=0*u.kNm
                dNsdi=math.cos(beta)*deltainitN
                dMsdi=math.sin(beta)*deltainitM
                while abs(dNsdi)>precisionN or abs(dMsdi)>precisionM:
                    Nsdi=Nsdi+dNsdi*alpha
                    Msdi=Msdi+dMsdi*alpha
                    print Msdi
                    tmp=self.fas.calc(Nsdi, Msdi, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, 0, 0, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
                    Apreqi=tmp['Ap']
                    Anreqi=tmp['An']
                    if Apreqi<=sect.Ap and Anreqi<=sect.An:
                        nextalpha=1.0
                    else:
                        nextalpha=-1.0
                    if (Nsdi*dNsdi).asNumber()<0 or (Msdi*dMsdi).asNumber()<0:
                        Nsdi=0*u.kN
                        Msdi=0*u.kNm
                        nextalpha=-alpha
                    if nextalpha*alpha==-1.0:
                        dNsdi = 0.5*dNsdi
                        dMsdi = 0.5*dMsdi
                    alpha=nextalpha
                    n=n+1
                Nrdi.append(Nsdi)
                Mrdi.append(Msdi)
            if sect.rysAn or sect.rysAp :
                Nsdi=0*u.kN
                Msdi=0*u.kNm
                dNsdi=math.cos(beta)*deltainitN
                dMsdi=math.sin(beta)*deltainitM
                while abs(dNsdi)>precisionN or abs(dMsdi)>precisionM:
                    Nsdi=Nsdi+dNsdi*alpha
                    Msdi=Msdi+dMsdi*alpha
                    tmp=self.fas.calc(Nsdi, Msdi, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
                    Apreqi=tmp['Ap']
                    Anreqi=tmp['An']
                    if Apreqi<=sect.Ap and Anreqi<=sect.An:
                        nextalpha=1.0
                    else:
                        nextalpha=-1.0
                    if (Nsdi*dNsdi).asNumber()<0 or (Msdi*dMsdi).asNumber()<0:
                        Nsdi=0*u.kN
                        Msdi=0*u.kNm
                        nextalpha=-alpha
                    if nextalpha*alpha==-1.0 :
                        dNsdi = 0.5*dNsdi
                        dMsdi = 0.5*dMsdi
                    alpha=nextalpha
                    n=n+1
                Nrdi_withcrackcontrol.append(Nsdi)
                Mrdi_withcrackcontrol.append(Msdi)
        failurecodei=0
        sect.resist_forcetomoment={'Nrdi':Nrdi, 'Mrdi':Mrdi, 'failurecode':failurecode}
        sect.resist_forcetomoment_withcrackcontrol={'Nrdi':Nrdi_withcrackcontrol, 'Mrdi':Mrdi_withcrackcontrol, 'failurecode':failurecode}
        return sect

    def As_as_forcefunction(self, sect, fromNsd=0*u.N, toNsd=10000000*u.N, dividenumber=30, acompMsd=0*u.Nm):
        Nsdrange=[None]*dividenumber
        for i in xrange(0, len(Nsdrange)):
            Nsdrange[i]=fromNsd+(1.0*toNsd-fromNsd)/(len(Nsdrange)-1)*i
        Ap=[None]*dividenumber
        An=[None]*dividenumber
        for i in xrange(0, len(Nsdrange)):
            tmp=self.fas.calc(Nsdrange[i], acompMsd, sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
            An[i]=tmp['An']
            Ap[i]=tmp['Ap']
        #print {'An':An, 'Ap':Ap, 'Nsdrange':Nsdrange, 'failurecode':[None]*dividenumber, 'acompMsd':acompMsd}
        sect.As_as_forcefunction={'An':An, 'Ap':Ap, 'Nsdrange':Nsdrange, 'failurecode':[None]*dividenumber, 'acompMsd':acompMsd}
        return sect
    
    def As_as_momentfunction(self, sect, fromMsd=-2000000*u.Nm, toMsd=2000000*u.Nm, dividenumber=100, acompNsd=0*u.N):
        Msdrange=[None]*dividenumber
        for i in xrange(0, len(Msdrange)):
            Msdrange[i]=fromMsd+(1.0*toMsd-fromMsd)/(len(Msdrange)-1)*i     
        Ap=[None]*dividenumber
        An=[None]*dividenumber
        for i in xrange(0, len(Msdrange)):
            tmp=self.fas.calc(acompNsd, Msdrange[i], sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
            Ap[i]=tmp['Ap']
            An[i]=tmp['An']
        #print {'An':An, 'Ap':Ap, 'Msdrange':Msdrange, 'failurecode':[None]*dividenumber, 'acompNsd':acompNsd}
        sect.As_as_momentfunction={'An':An, 'Ap':Ap, 'Msdrange':Msdrange, 'failurecode':[None]*dividenumber, 'acompNsd':acompNsd}
        return sect
    
    def As_as_forcetomomentfunction(self, sect, fromNsd=-1000000*u.N, toNsd=9000000*u.N, dividenumberNsd=10, fromMsd=-1000000*u.Nm, toMsd=1000000*u.Nm, dividenumberMsd=10):
        deltaNsd=(1.0*toNsd-fromNsd)/dividenumberMsd
        deltaMsd=(1.0*toMsd-fromMsd)/dividenumberNsd  
        Nsd=[[0]*(dividenumberMsd+1)]
        Msd=[[0]*(dividenumberMsd+1)]
        Ap=[[0]*(dividenumberMsd+1)]
        An=[[0]*(dividenumberMsd+1)]   
        for i in xrange(0, dividenumberNsd):
            Nsd.append([0]*(dividenumberMsd+1))
            Msd.append([0]*(dividenumberMsd+1))
            Ap.append([0]*(dividenumberMsd+1))
            An.append([0]*(dividenumberMsd+1))
        for i in xrange(0, dividenumberNsd+1):
            for j in xrange(0, dividenumberMsd+1):
                Nsd[i][j]=fromNsd+(1.0*toNsd-fromNsd)/dividenumberNsd*i
                Msd[i][j]=fromMsd+(1.0*toMsd-fromMsd)/dividenumberMsd*j
        for i in xrange(0, dividenumberNsd+1):
            for j in xrange(0, dividenumberMsd+1):
                tmp=self.fas.calc(Nsd[i][j], Msd[i][j], sect.h, sect.b, sect.ap, sect.an, sect.fip, sect.fin, sect.rysAn, sect.rysAp, sect.wlimp, sect.wlimn, sect.fcd, sect.fctm, sect.fyd)
                Ap[i][j]=tmp['Ap']
                An[i][j]=tmp['An']
        #print {'An':An, 'Ap':Ap, 'Nsd':Nsd, 'Msd':Msd, 'failurecodei':None}
        sect.As_as_forcetomomentfunction={'An':An, 'Ap':Ap, 'Nsd':Nsd, 'Msd':Msd, 'failurecodei':None}
        return sect
    
# Test if main
if __name__ == '__main__':
    print ('test RcRecSectSolver')
    sec=RcRecSect()
    solv=RcRecSectSolver()
    load=SectLoad()
    load.add_loadcase()
    sec.Ap=20*u.cm2
    sec.An=20*u.cm2
    print ('--------------------reinforce(self, sect, load)--------------------')
    print sec.get_sectinfo()
    solv.paraminfo()
    print load.get_loadcases()
    load.edit_loadcase(0, {"Name": 'ULS_changed', "Msd": 1200*u.Nm, "MTsd": 2*u.Nm, "Nsd": 0*u.N, "Vsd": 9*u.N})
    load.add_loadcase({"Name": 'ULS_new', "Msd": 800*u.kNm, "MTsd": 2*u.Nm, "Nsd": 0*u.N, "Vsd": 9*u.N})
    print load.get_loadcases()
    print ('-----------------1-----------------------')
    sec=solv.reinforce(sec,load)
    print ('-----------------2-----------------------')
    print sec.get_sectinfo()
    print ('-----------------solv.resist_moment(sec)-----------------------')
    print solv.resist_moment(sec)
    print ('-----------------solv.resist_force(sec)-----------------------')
    print solv.resist_force(sec)
    print ('-----------------solv.As_as_forcefunction(sec)-----------------------')
    print solv.As_as_forcefunction(sec)
    print ('-----------------solv.As_as_forcefunction(sec)-----------------------')
    print solv.As_as_forcefunction(sec)
    print ('-----------------solv.As_as_momentfunction(sec)-----------------------')
    print solv.As_as_momentfunction(sec)
    print ('-----------------solv.As_as_forcetomomentfunction(sec)-----------------------')
    a = solv.As_as_forcetomomentfunction(sec)
    print a.As_as_forcetomomentfunction['Nsd']
    print a.As_as_forcetomomentfunction['Msd']
    print a.As_as_forcetomomentfunction['Ap']
    print a.As_as_forcetomomentfunction['An']
    print ('-----------------resist_forcetomoment(sect, dividenumber=10))-----------------------')
    a = solv.resist_forcetomoment(sec, 10)
    print a.resist_forcetomoment
    print sec.Ap
    print sec.An
    a.rysAn=1
    a.rysAp=1
    a.plot_resist_forcetomoment(load)



