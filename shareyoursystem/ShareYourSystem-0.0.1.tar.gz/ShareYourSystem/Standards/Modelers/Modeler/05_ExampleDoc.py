
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyModeler=SYS.ModelerClass(
		**{
			'FolderingPathVariable':SYS.Modeler.LocalFolderPathStr,
			'HdformatingFileKeyStr':'Thing2.hdf',
			'ModelingDescriptionTuplesList':
			[
				#GetStr #ColumnStr #Col
				('MyStr','MyStr',SYS.tables.StringCol(10)),
				('MyIntsList','MyIntsList',SYS.tables.Int64Col(shape=3))
			]	
		}
	).model(
	)

#Build a structure with a database
SYS.mapSet(
		MyModeler.ModeledHdfTable,
		[
			('row.__setitem__',{'#liarg':('MyStr',"hello")}),
			('row.append',{'#liarg':None}),
			('row.__setitem__',{'#liarg':('MyStr',"bonjour")}),
			('row.__setitem__',{'#liarg':('MyIntsList',[4,5,6])}),
			('row.append',{'#liarg':None}),
			('flush',{'#liarg':None})
		]
)

#Definition the AttestedStr
print('MyModeler is ')
SYS._print(MyModeler)

#view
print('hdf5 file is : \n'+SYS._str(MyModeler.hdfview()))

#close
MyModeler.file(_ModeStr='c')


