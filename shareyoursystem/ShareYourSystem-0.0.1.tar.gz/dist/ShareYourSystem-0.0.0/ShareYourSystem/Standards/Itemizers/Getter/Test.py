#ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Getter

#Test
#Getter.GetterClass().notebook('Readme')

#Getter.GetterClass().cell()

import os
#help(os.path.walk)

def test(_LiargVariablesList,_FolderPathStr,_DirKeyStrsList):
	print(_LiargVariablesList,_FolderPathStr,_DirKeyStrsList)




os.path.walk(os.getcwd(),test,[])