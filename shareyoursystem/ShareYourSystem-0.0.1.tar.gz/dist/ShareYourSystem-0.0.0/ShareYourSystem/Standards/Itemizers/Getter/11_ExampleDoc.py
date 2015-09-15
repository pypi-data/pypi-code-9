
#ImportModules
import ShareYourSystem as SYS

#Define
MyGetter=SYS.GetterClass(
	).get(
		{
			'#key':'MyDict',
			'#set':('MyStr',"hello")
		}
	)

MyGetter.get(
		{
			'#key':'YourDict',
			'#map@set':{
				'MyStr':"bonjour",
				'MyFloat':0.5
			}
		}
	)

#print
print('MyGetter is ')
SYS._print(MyGetter)
