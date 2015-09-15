# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>

The Classors help for decorating a Class. 
Here are defined the important derived Objects that
facilitates the manners to set a new defined Class in the 
SYS scope and set automatically into it new 'boilerplates'
methods like the 'default_init' (cf. Defaultor),'do_<DoMethodStr>'
 (cf. Doer), 'mimic_<DoMethodStr>' (cf. Mimicker), also
 decorates methods for making it switch or resetting.

"""

#<DefineConcept>
import ShareYourSystem as SYS
SYS.setConceptModule(globals())
#</DefineConcept>

#import
from ShareYourSystem.Standards.Classors import Classor
