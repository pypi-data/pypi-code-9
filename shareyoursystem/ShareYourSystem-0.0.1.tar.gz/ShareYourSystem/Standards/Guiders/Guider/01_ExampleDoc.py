
#ImportModules
import ShareYourSystem as SYS

#Definition an instance
MyGuider=SYS.GuiderClass(
	).folder(
		SYS.Filer
	).guide(
		#GuidingIndexStr
		'001',
		#GuidingPageStr
		'Github',
		#GuidingBookStr
		'Doc',
		#GuidingScriptStr
		'Markdown'
	)
		
#Definition the AttestedStr
print('MyGuider is ')
SYS._print(MyGuider)
