
#ImportModules
import ShareYourSystem as SYS

#Define
MyParenter=SYS.ParenterClass(
	).array(
		[
			['-Children'],
			['|Aurelie'],
			['-GrandChildren'],
			['|Anton','|Loup'],
		]
	)

#print
print('MyParenter is ')
SYS._print(MyParenter)