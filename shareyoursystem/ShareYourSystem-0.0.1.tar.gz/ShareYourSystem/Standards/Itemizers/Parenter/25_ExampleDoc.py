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
	).parentDown(
	)

#print
print('MyParenter is ')
SYS._print(MyParenter)


