
#ImportModules
import ShareYourSystem as SYS

#define and get two children
MyParenter=SYS.ParenterClass(
	).array(
		['/&Neurons/$First','/&Neurons/$Second']
	).command(
		'/&Clients/$First',
		(
			'point',
			[
				'/^/&Neurons/$Second',
				'/&Connections/$FirstToSecond/'
			]
		)
	)

#print
print('MyParenter is ')
SYS._print(MyParenter)

