#ImportModules
import ShareYourSystem as SYS

#Definition 
MyFindoer=SYS.FindoerClass(
		**{
			'FolderingPathVariable':SYS.Findoer.LocalFolderPathStr,
			'HdformatingFileKeyStr':'Thing.hdf',
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
			'MyIntsList':[0,0,1]
		}
	).insert(
	).find(
		#FindingWhereVariable
		[
			('MyInt',(SYS.operator.eq,0)),
			('MyIntsList',(SYS.getIsEqualBool,[2,4,1]))
		],
		#FindingRecoverBool
		True
	)

#print
print('MyFindoer is ')
SYS._print(MyFindoer)

#view
print('hdf5 file is : \n'+SYS._str(MyFindoer.hdfview()))

#close
MyFindoer.file(_ModeStr='c')

