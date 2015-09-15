#ImportModules
import ShareYourSystem as SYS

#Definition a Nbconverter
MyNbconverter=SYS.NbconverterClass(
	).folder(
		SYS.Classor
	).scriptbook(
		**{
			'GuidingBookStr':'Doc'
		}
	).notebook(
		'Presentation.ipynb'
	).nbconvert(
		'Readme.md'
	)
		
#Definition the AttestedStr
print('MyNbconverter is ')
SYS._print(MyNbconverter)  



