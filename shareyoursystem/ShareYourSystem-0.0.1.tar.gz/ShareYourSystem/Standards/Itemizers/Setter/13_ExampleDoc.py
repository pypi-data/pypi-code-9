
#ImportModules
import ShareYourSystem as SYS

#Define and set a dict
MySetter=SYS.SetterClass(
	)['#map@set'](
		{
			'MyStr':"hello",
			'#bound:printHello':lambda _SelfVariable:SYS._print(_SelfVariable.MyStr)
		}
	)

#change the MyStr
MySetter.MyStr="bonjour"

#printHello
MySetter.printHello()