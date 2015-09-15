
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
				('MyInt','MyInt',SYS.tables.Int64Col()),
				('MyFloatsList','MyFloatsList',(SYS.tables.Float64Col,['UnitsInt']))
			],
			'RowingKeyStrsList':[
				'MyInt',
				'MyFloatsList'
			]
		}
	).model(
	).mapSet(
		{
			'MyInt':1,
		}
	).insert(
	).mapSet(
		{
			'MyInt':1,
			'MyFloatsList':[0.,1.,2.]
		}
	).insert(
	).mapSet(
		{
			'MyInt':5,
			'MyFloatsList':[0.,0.]
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


