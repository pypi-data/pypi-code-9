
#ImportModules
import ShareYourSystem as SYS

#Definition of a Scriptbooker
MyScriptbooker=SYS.ScriptbookerClass(
	).folder(
		SYS.Filer
	).scriptbook(
		**{
			'GuidingBookStr':'Doc'
		}
	)

#Definition the AttestedStr
print('MyScriptbooker is ')
SYS._print(MyScriptbooker)


