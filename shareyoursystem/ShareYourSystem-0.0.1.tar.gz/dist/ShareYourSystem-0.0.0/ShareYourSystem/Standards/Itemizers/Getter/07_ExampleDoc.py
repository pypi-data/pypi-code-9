
#ImportModules
import ShareYourSystem as SYS

#Define
MyGetter=SYS.GetterClass()
MyGetter.MyInt=1
MyGetter.HelloStr="hello"
MyGetter.FirstRedirectStr="HelloStr"
MyGetter.SecondRedirectStr="FirstRedirectStr"

#print
print('A simple dict get with key MyInt gives')
SYS._print(MyGetter[{"#key":"MyInt"}])

#print
print('A first undirect level get gives with #key:#get')
SYS._print(MyGetter[{"#key:#get":"FirstRedirectStr"}])

#print
print('A recursive undirect level get gives')
SYS._print(MyGetter[
		{
			"#key:#get":{
				"#key:#get":"SecondRedirectStr"
			}
		}
	]
)

#print
print("A dict map get is like this")
SYS._print(MyGetter[{'#key:#map@get':['MyStr','MyInt']}])

