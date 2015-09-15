
#ImportModules
import ShareYourSystem as SYS

#Explicit expression
MyPather=SYS.PatherClass(
	)['#map@set'](
		{
			'/ChildPather/GrandChildPather':{
				'MyInt':0
			}
		}
	)


#print
print('MyPather is ')
SYS._print(MyPather)