
#ImportModules
import ShareYourSystem as SYS

#Definition 
MyModeler=SYS.ModelerClass(
		**{
			'FolderingPathVariable':SYS.Modeler.LocalFolderPathStr,
			'HdformatingFileKeyStr':'Thing1.hdf',
			'ModelKeyStrsList':[	
				'MyStr',
				'MyIntsList'
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
			('row.__setitem__',{'#liarg':('MyIntsList',[1])}),
			('row.append',{'#liarg':None}),
			#('row.__setitem__',{'#liarg':('MyStr',"bonjour")}), 
			#('row.__setitem__',{'#liarg':('MyIntsList',[1,3])}), 
			#THIS would bring an error because list has to be size=1
			#('row.append',{'#liarg':None}),
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


