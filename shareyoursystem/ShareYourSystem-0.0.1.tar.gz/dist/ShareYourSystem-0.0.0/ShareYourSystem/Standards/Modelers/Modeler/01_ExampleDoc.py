#ImportModules
import ShareYourSystem as SYS

#Definition 
MyModeler=SYS.ModelerClass(
		**{
			'FolderingPathVariable':SYS.Modeler.LocalFolderPathStr,
			'PymongoingDatabaseStr':"Thing"
		}
	).model(
	)

#Build a structure with a database
SYS.mapSet(
		MyModeler.ModeledMongoCollection,
		[
			('remove',{}),
			('insert',{'MyStr':"hello"})
		]
)

#print
print('mongo db is : \n'+SYS._str(MyModeler.pymongoview()))

#print
print('MyModeler is ')
SYS._print(MyModeler)

#kill
MyModeler.process(_ActionStr='kill')
