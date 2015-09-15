#ImportModules
import ShareYourSystem as SYS

#define structure
MyParenter=SYS.ParenterClass(
	).array(
		[
			['-Outlets','-Inlets'],
			['|A','|B'],
			['-Outlets','-Inlets'],
			['|A','|B']
		]
	)

#parentUp
MyParenter['/-Outlets/|A/-Outlets/|A'].parentUp()

#print
print('MyParenter is ')
SYS._print(MyParenter)


