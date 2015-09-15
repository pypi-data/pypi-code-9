
#ImportModules
import ShareYourSystem as SYS

#define and build a chain
MyCommander=SYS.CommanderClass(
	).get(
		'/ChildCommander/ChildCommander'
	)

#just command at the first level
MyCommander['--ChildCommander']={
			'MyInt':0
		}

#command then walk after
MyCommander['--...ChildCommander']={
			'MyStr':"hello"
		}

#walk before then command 
MyCommander['...--ChildCommander']={
			'MyFloat':0.1
		}

#set self before then walk before then command 
MyCommander['/...--ChildCommander']={
			'MyList':[0.1]
		}

#walk before then command then set after
MyCommander['.../--ChildCommander']={
			'MyBool':False
		}

#print
print('MyCommander is ')
SYS._print(MyCommander)