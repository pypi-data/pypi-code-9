
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyFindoer=SYS.FindoerClass(
		**{
			'FolderingPathVariable':SYS.Findoer.LocalFolderPathStr,
			'PymongoingDatabaseStr':"Thing",
			'ModelKeyStrsList':
			[
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
	).find(
		#FindingWhereVariable
		{
			'MyInt':{'$gt':1},
			'MyIntsList':[0,0,1]
		}
	)
				
#Definition the AttestedStr
print('MyFindoer is ')
SYS._print(MyFindoer) 

#print
print('mongo db is : \n'+SYS._str(MyFindoer.pymongoview()))

#Print
MyFindoer.file(_ModeStr='c')


