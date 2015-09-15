
#ImportModules
import ShareYourSystem as SYS

#Definition a Pymongoer 
MyPymongoer=SYS.PymongoerClass(
	).pymongo(
		**{
			'FolderingPathVariable':SYS.Pymongoer.LocalFolderPathStr
		}
	)

#remove
MyPymongoer.PymongoneClientVariable['MyDatabase']
MyPymongoer.PymongoneClientVariable.MyDatabase.ThingsCollection.remove({})
MyPymongoer.PymongoneClientVariable.MyDatabase.ThingsCollection.insert({'MyStr':'hello'})

#Definition the AttestedStr
SYS._print('MyPymongoer is '+SYS._str(MyPymongoer)+'\n')

#print
print('ThingsCollection fetch gives')
SYS._print(
	MyPymongoer.pymongoview('MyDatabase')
)

#close
MyPymongoer.process(_ActionStr='kill')

