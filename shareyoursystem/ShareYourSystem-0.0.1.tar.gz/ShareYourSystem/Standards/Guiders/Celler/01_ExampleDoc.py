
#ImportModules
import ShareYourSystem as SYS

#Definition an instance
MyCeller=SYS.CellerClass(
	).file(
			_ModeStr='r',
		**{
			'FolderingPathVariable':
			SYS.ShareYourSystemLocalFolderPathStr+'Pythonlogy/ShareYourSystem/Standards/Interfacers/Filer/',
			'FilingKeyStr':'01_ExampleDoc.py'
		}
	).cell(
		_ScriptStr='Python'
	)
		
#Definition the AttestedStr
print('MyCeller is ')
SYS._print(MyCeller)

