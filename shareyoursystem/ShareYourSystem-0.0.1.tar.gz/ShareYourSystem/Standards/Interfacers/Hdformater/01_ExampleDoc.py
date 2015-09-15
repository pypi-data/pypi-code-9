
#ImportModules
import ShareYourSystem as SYS

#Definition a Hdformater that writes an empty hdf file
MyHdformater=SYS.HdformaterClass(
	).hdformat(
		#HdformatingFileKeyStr
		'Hdformats.hdf5',
		**{
			'FolderingPathVariable':SYS.Hdformater.LocalFolderPathStr
		}
	)

#Set reactively groups inside
MyHdformater.HdfGroupPathStr='/ChildGroup/GrandChildGroup'

#Definition the AttestedStr
print('MyHdformater.HdformatedConsoleStr is ')
SYS._print(MyHdformater.hdfview())

#close
MyHdformater.file(_FilingModeStr='c')




