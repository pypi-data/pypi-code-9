
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyModeler=SYS.ModelerClass(
		).mapSet(
			{
				'FolderingPathVariable':SYS.Modeler.LocalFolderPathStr,
				'HdformatingFileKeyStr':'Stuff.hdf',
				'UnitsInt':3,
				'ModelingDescriptionTuplesList':
				[
					#GetStr #ColumnStr #Col
					('MyInt','MyInt',SYS.tables.Int64Col()),
					('MyFloatsList','MyFloatsList',(SYS.tables.Float64Col,['UnitsInt']))
				]
			}
	).model(
	)

#Build a structure with a database
SYS.mapSet(
		MyModeler.ModeledHdfTable,
		[
			('row.__setitem__',{'#liarg':('MyInt',0)}),
			('row.append',{'#liarg':None}),
			('row.__setitem__',{'#liarg':('MyInt',2)}),
			('row.__setitem__',{'#liarg':('MyFloatsList',[0.,1.,2.])}),
			('row.append',{'#liarg':None}),
			('flush',{'#liarg':None})
		]
)

#Definition 
MyModeler.setDone(
		SYS.ModelerClass
	).setSwitch(
	).mapSet(
			{
				'UnitsInt':2,
				'ModelingDescriptionTuplesList':
				[
					#GetStr #ColumnStr #Col
					('MyInt','MyInt',SYS.tables.Int64Col()),
					('MyFloatsList','MyFloatsList',(SYS.tables.Float64Col,['UnitsInt']))
				]
			}
	).model(
	)

#Build a structure with a database
SYS.mapSet(
		MyModeler.ModeledHdfTable,
		[
			('row.__setitem__',{'#liarg':('MyInt',0)}),
			('row.append',{'#liarg':None}),
			('row.__setitem__',{'#liarg':('MyInt',2)}),
			('row.__setitem__',{'#liarg':('MyFloatsList',[0.,1.])}),
			('row.append',{'#liarg':None}),
			('flush',{'#liarg':None})
		]
)


#print
print('MyModeler is ')
SYS._print(MyModeler)

#view
print('hdf5 file is : \n'+SYS._str(MyModeler.hdfview()))

#close
MyModeler.file(_ModeStr='c')


