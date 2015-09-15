#ImportModules
import ShareYourSystem as SYS

#Definition 
MyRetriever=SYS.RetrieverClass(
		**{
			'FolderingPathVariable':SYS.Retriever.LocalFolderPathStr,
			'HdformatingFileKeyStr':"Thing.hdf",
			'ModelingDescriptionTuplesList':
			[
				#GetStr #ColumnStr #Col
				('MyInt','MyInt',SYS.tables.Int64Col()),
				('MyStr','MyStr',SYS.tables.StringCol(10)),
				('MyIntsList','MyIntsList',SYS.tables.Int64Col(shape=3))
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

#print
print('MyRetriever is ')
SYS._print(MyRetriever)

#view
print('hdf5 file is : \n'+SYS._str(MyRetriever.hdfview()))

#close
MyRetriever.file(_ModeStr='c')
