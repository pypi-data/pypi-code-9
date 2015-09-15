#ImportModules
import ShareYourSystem as SYS

#Definition of an instance Filer and make it find the current dir
MyFiler=SYS.FilerClass(
	).file(
		#FilingKeyStr
		'MyOpenedFile.txt',
		#FilingModeStr
		'w',
		**{
			'FolderingPathVariable':SYS.Filer.LocalFolderPathStr
		}
	).file(
		_ModeStr='c'
	)

#print
print('MyFiler is ')
SYS._print(MyFiler) 
