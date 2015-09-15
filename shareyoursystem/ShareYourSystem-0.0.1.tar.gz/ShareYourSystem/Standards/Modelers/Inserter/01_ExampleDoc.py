
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyInserter=SYS.InserterClass(
		**{
			'FolderingPathVariable':SYS.Inserter.LocalFolderPathStr,
			'PymongoingDatabaseStr':"Thing",
			'ModelKeyStrsList':[
				'MyInt',
				'MyStr',
				'MyIntsList'
			],
			'RowingKeyStrsList':[
				'MyInt',
				'MyStr'
			]
		}
	).model(
	).mapSet(
		{
			'MyInt':0,
			'MyStr':"hello",
			'MyIntsList':[2,4,1]
		}
	).insert(
	).mapSet(
		{
			'MyInt':5,
			'MyStr':"bonjour",
			'MyIntsList':[0,0,1]
		}
	).insert(
	)
	
#print
print('mongo db is : \n'+SYS._str(MyInserter.pymongoview()))

#print
print('MyInserter is ')
SYS._print(MyInserter)

#Print
MyInserter.process(_ActionStr='kill')



