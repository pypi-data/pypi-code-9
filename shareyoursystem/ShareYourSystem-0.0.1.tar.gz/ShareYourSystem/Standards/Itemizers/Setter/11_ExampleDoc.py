
#ImportModules
import ShareYourSystem as SYS

#Define and set with #key dict for the KeyVariable
MySetter=SYS.SetterClass(
	).set(
		'MyStr',
		'HelloStr'
	).set(
		{'#key':"MyStr"},
		"hello"
	)

#Define and set with a #get in the value
MySetter.set(
		"FirstCloneMyStr",
		'#get:MyStr'
	)

#Define and set with a recursive #get in the value
MySetter.set(
		"FirstCloneHelloStr",
		'#get:#get:MyStr'
	)

#Define and set with a #value dict for the ValueVariable
MySetter.set(
		"RedirectStr",
		{'#value':'MyStr'}
	)

#Define and set with a #value dict for the ValueVariable
MySetter.set(
		"MyDict",
		{'#value':{'MyInt':0}}
	)

#Define and set with a #value:#get dict for the ValueVariable
MySetter.set(
		"SecondCloneStr",
		{'#value:#get':'MyStr'}
	)

#Define and set with a #value:#map@get dict for the ValueVariable
MySetter.set(
		"MyList",
		{'#value:#map@get':['MyStr','MyInt','#direct:FooStr']}
	)

#Define and set with a #value:#map@get dict for the ValueVariable
MySetter.set(
		MySetter.MyList.append,
		{'#value':'MyStr'}
	)

#Define and set with a #value:#map@get dict for the ValueVariable
MySetter.set(
		MySetter.MyList.append,
		{'#value:#map@get':['MyInt']}
	)

#print
print('MySetter is ')
SYS._print(MySetter)
