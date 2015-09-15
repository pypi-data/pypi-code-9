#ImportModules
import ShareYourSystem as SYS


#Definition of an instance Folderer and make it find the current dir
MyFolderer=SYS.FoldererClass(
	).folder(
		#FolderingPathVariable
		SYS.Folderer.LocalFolderPathStr
	)


#If you don't have these folder, MyFolderer is going to create them for you
MyFolderer.folder(
		#FolderingPathVariable
		MyFolderer.FolderingPathVariable+'TestFolder1/TestFolder2/',
		#FolderingMkdirBool
		True
	)	

#Definition the AttestedStr
print('MyFolderer is ')
SYS._print(MyFolderer)

