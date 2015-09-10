import os
import pySAXS
from pySAXS.filefilters import fileimport

ff=fileimport.fileImport('saxs')
q,i,err=ff.read(pySAXS.__path__[0]+os.sep+"saxsdata"+os.sep+"OT-2014-03-31-45d10-3600s.tif.rgr")

    
from pySAXS.models import SphereGaussAnaDC
d=SphereGaussAnaDC() #declare model
d.Arg=[300.000000,40.0,4.218e+15,2e11,1e10] #initial parameters
d.q=q
res=d.fit(i)
print res
