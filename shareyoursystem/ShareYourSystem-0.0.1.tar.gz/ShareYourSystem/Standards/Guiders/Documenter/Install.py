#ImportModules
import os
import ShareYourSystem as SYS
from ShareYourSystem.Guiders import Installer

#Definition an Installer instance
MyInstaller=Installer.InstallerClass(**{
	'GuidingBookStr':'Doc',
	'DirectingFilterFunctionPointer':
		lambda _InstanceVariable,_FolderKeyStr:_FolderKeyStr.startswith('_'
		)==False
	}
)

#map
map(
	MyInstaller.install,
	[
		#os.getcwd()
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Objects/Object',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Objects/Caller'
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Objects',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Classors',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Interfacers',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Guiders',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Itemizers',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Applyiers',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Walkers',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Noders',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Savers',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Databasers',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Ploters',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Tutorials',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Simulaters',
		#SYS.ShareYourSystemLocalFolderPathStr+'/ShareYourSystem/Muzikers',
	]
)

