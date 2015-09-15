
#ImportModules
import ShareYourSystem as SYS

#define and team
MyTeamer=SYS.TeamerClass(
	).team(
		#TeamingKeyStr
		"Employees"
	)

#Define and team with specifying the Variable
MyTeamer.team(
		#TeamingKeyStr
		'Partners',
		#TeamingValueVariable
		SYS.CommanderClass()
	)

#With a set
MyTeamer['-Clients']=SYS.CommanderClass()

#With also a team insert
MyTeamer.team(
		'Collegues',
		_IndexInt=1
	)


#print
print('MyTeamer is ')
SYS._print(MyTeamer)

#Shortcut for getting all the teamed instances
print("MyTeamer['-'] is ")
SYS._print(MyTeamer['-'])

#Shortcut for getting all the teamed instances
print("MyTeamer['-.values'] is ")
SYS._print(MyTeamer['-.values'])

#Shortcut for getting all the teamed instances
print("MyTeamer['-.keys'] is ")
SYS._print(MyTeamer['-.keys'])

#print
print("MyTeamer['-Clients'].TeamIndexInt is ")
print(MyTeamer['-Clients'].TeamIndexInt)
