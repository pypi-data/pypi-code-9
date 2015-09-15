# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Databasers defines the Noders that take the role of 
the client-side "Model" in the MVC architecture of SYS. 
Here the databasing process relies on a hdf5 
pytable wrapping, going from simple encapsulations
of the create_table,insert methods to 'sophisticated'
routines that facilitate the joins between tables and 
the automatic shaping of the rowed datas.

Why hdf5 compared to a simple binary files saving ?

-hdf5 file is one key node to get all the subfolders and file data making
the copy,delete,mv easier.

-it makes also simple the constrains linked to the reading modes,
because we can easy make a copy for reading and keep another for 
continuing storing. (...classical db server problem)

-key nodes (or groups) inside of an hdf5 can be so long as we wish
compared to classic folder or file name length constrain on Mac, Linux, Windows.

-hdf5 has modules for storing like tables, so
the naming process for a set of data is considerably 
lighted.

-hdf5 is on the way to have specialized library to get you
read with the automatic join and hierarchy problem between 
tables.


"""

#<DefineConcept>
import ShareYourSystem as SYS
SYS.setConceptModule(globals())
#</DefineConcept>
