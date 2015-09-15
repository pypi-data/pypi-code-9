
#ImportModules
import ShareYourSystem as SYS

#Define
MyGetter=SYS.GetterClass()
MyGetter.MyInt=1

#get and modify
NewInt=MyGetter[
	{
		'#key':"MyInt",
		'#modify':SYS.GetClass(
			lambda _SelfVariable:_SelfVariable.GettedValueVariable+1
		)
	}
]

#print
print('NewInt is '+str(NewInt))
