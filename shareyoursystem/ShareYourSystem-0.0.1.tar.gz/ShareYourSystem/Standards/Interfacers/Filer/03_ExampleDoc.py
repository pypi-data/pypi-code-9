#ImportModules
import ShareYourSystem as SYS

#Definition of an instance Filer and make it find the current dir
MyFiler=SYS.FilerClass().file(
	'MyWrittenFile.txt',
	'w',
	_WriteVariable="hello",
	**{
		'FolderingPathVariable':SYS.Filer.LocalFolderPathStr,
	}
	).file(
		_ModeStr='c'
	)
	
#Definition the AttestedStr
print('MyFiler is ')
SYS._print(MyFiler)


