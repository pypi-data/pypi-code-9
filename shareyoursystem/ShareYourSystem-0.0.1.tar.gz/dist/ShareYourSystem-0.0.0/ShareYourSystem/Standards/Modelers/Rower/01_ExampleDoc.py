
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyRower=SYS.RowerClass(
		**{
			'FolderingPathVariable':SYS.Rower.LocalFolderPathStr,
			'ModelKeyStrsList':['MyInt','MyStr','MyIntsList']	
		}
	).model(
	).mapSet(
		{
			'MyInt':0,
			'MyStr':"hello",
			'MyIntsList':[2,4,1]
		}
	).row(
	)
	
#Build a structure with a database
SYS.mapSet(
		MyRower.ModeledMongoCollection,
		[
			('remove',{}),
			('insert',{'MyStr':"hello"})
		]
)

#print
print('mongo db is : \n'+SYS._str(MyRower.pymongoview()))

#print
print('MyRower is ')
SYS._print(MyRower)

#Print
MyRower.process(_ActionStr='kill')



