
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyRetriever=SYS.RetrieverClass(
		**{
			'FolderingPathVariable':SYS.Retriever.LocalFolderPathStr,
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
			'MyIntsList':[0,0,0]
		}
	).insert(
	).retrieve(
		#RetrievingIndexIntsList
		[0,0]	
	)
		
#Definition the AttestedStr
print('MyRetriever is ')
SYS._print(MyRetriever) 

#print
print('mongo db is : \n'+SYS._str(MyRetriever.pymongoview()))

#Print
MyRetriever.file(_ModeStr='c')
