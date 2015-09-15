#ImportModules
import ShareYourSystem as SYS

#Definition a Notebooker
MyNotebooker=SYS.NotebookerClass(
	).folder(
		SYS.Filer
	).scriptbook(
		**{
			'GuidingBookStr':'Doc'
		}
	).notebook(
		#NotebookingFileKeyStr
		'Presentation.ipynb'
	)

#Definition the AttestedStr
print('MyNotebooker is ')
SYS._print(MyNotebooker)






