#ImportModules
import ShareYourSystem as SYS

#Definition of an instance Processer and make it print hello
MyProcesser=SYS.ProcesserClass(
	).process(
		#ProcessingBashStr
		'which python ',
		#ProcessingDirectStr
		False,
		**{
			'FolderingPathVariable':SYS.Processer.LocalFolderPathStr
		}
	)
		
#Define
print('MyProcesser.ProcessedBashStr is ')
SYS._print(MyProcesser.ProcessedBashStr)
	



