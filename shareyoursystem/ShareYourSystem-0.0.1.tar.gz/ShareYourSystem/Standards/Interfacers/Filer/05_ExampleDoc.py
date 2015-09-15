#ImportModules
import ShareYourSystem as SYS

#Definition of an instance Filer and make it find the current dir
MyFiler=SYS.FilerClass(
	).file(
		'MyReadedFile.txt',
		'w',
		_WriteVariable='saluuut'
	).file(
		_ModeStr='r'
	).file(
		_ModeStr='c'
	)
	
#Definition the AttestedStr
print('MyFiler.FiledReadVariable is ')
SYS._print(MyFiler.FiledReadVariable)


