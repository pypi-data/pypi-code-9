
#ImportModules
import ShareYourSystem as SYS

#define
MyParenter=SYS.ParenterClass(
	).team(
		'Children',
		{
			'MyInt':0,
			'manage':['Aurelie']
		}
	).team(
		'Clients',
		{
			'MyStr':"hello"
		}
	)

#print
print("MyParenter is ")
SYS._print(MyParenter)





