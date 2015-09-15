
#ImportModules
import ShareYourSystem as SYS

#Define config
MyInserter=SYS.InserterClass(
		**{
			'FolderingPathVariable':SYS.Inserter.LocalFolderPathStr,
			'HdformatingFileKeyStr':'ThingAndStuff.hdf5',
			'ModelingDescriptionTuplesList':
			[
				#GetStr #ColumnStr #Col
				('MyStr','MyStr',SYS.tables.StringCol(10)),
				('MyIntsList','MyIntsList',SYS.tables.Int64Col(shape=3))
			],
			'RowingKeyStrsList':[
					'MyStr',
					'MyIntsList'
			]	
		}
	).model(
	).mapSet(
		{
			'MyStr':"hello",
			'MyIntsList':[2,4,1]
		}
	).insert(
	).mapSet(
		{
			'MyStr':"bonjour",
			'MyIntsList':[0,0,1]
		}
	).insert(
	)

#print
print('MyInserter is ')
SYS._print(MyInserter)

#view
print('hdf5 file is : \n'+SYS._str(MyInserter.hdfview()))

#close
MyInserter.file(_ModeStr='c')



