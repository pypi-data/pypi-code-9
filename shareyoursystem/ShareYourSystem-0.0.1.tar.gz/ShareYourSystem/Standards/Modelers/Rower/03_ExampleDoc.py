
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyRower=SYS.RowerClass(
		**{
			'FolderingPathVariable':SYS.Rower.LocalFolderPathStr,
			'HdformatingFileKeyStr':'Things.hdf',
			'ModelingDescriptionTuplesList':
				[
					#GetStr #ColumnStr #Col
					('MyInt','MyInt',SYS.tables.Int64Col()),
					('MyStr','MyStr',SYS.tables.StringCol(10)),
					('MyIntsList','MyIntsList',SYS.tables.Int64Col(shape=3))
				]	
		}
	).mapSet(
		{
			'MyInt':0,
			'MyStr':"hello",
			'MyIntsList':[2,4,1]
		}
	).row(
	)

#Definition the AttestedStr
print('MyRower is ')
SYS._print(MyRower)

#view
print('hdf5 file is : \n'+SYS._str(MyRower.hdfview()))

#close
MyRower.file(_ModeStr='c')

