
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.ClasserClass()
class MakerClass(SYS.ModelerClass):

	def default_init(self,
			_MakingMyInt=3,
			_MakingMyIntsList={
							'DefaultValueType':property,
							'PropertyInitVariable':None,
							'PropertyDocStr':'I am doing the thing here',
							'ShapeKeyStrsList':['MakingMyInt']
						},
			**_KwargVariablesDict	
		):
		SYS.ModelerClass.__init__(self,**_KwargVariablesDict)

#Definition 
MyMaker=MakerClass(
		**{
			'FolderingPathVariable':SYS.Modeler.LocalFolderPathStr,
			'HdformatingFileKeyStr':'Make.hdf',
			'ModelKeyStrsList':['MyStr','MakingMyIntsList']
		}
	).model(
	)

#Build a structure with a database
SYS.mapSet(
		MyMaker.ModeledHdfTable,
		[
			('row.__setitem__',{'#liarg':('MyStr',"hello")}),
			('row.append',{'#liarg':None}),
			('row.__setitem__',{'#liarg':('MyStr',"bonjour")}),
			('row.__setitem__',{'#liarg':('MakingMyIntsList',[0,4,5])}),
			('row.append',{'#liarg':None}),
			('flush',{'#liarg':None})
		]
)

#print
print('MyMaker is ')
SYS._print(MyMaker)

#view
print('hdf5 file is : \n'+SYS._str(MyMaker.hdfview()))

#close
MyMaker.file(_ModeStr='c')





