
#ImportModules
import ShareYourSystem as SYS

#Define
class ChildClass(SYS.TeamerClass):pass
class ChildrenClass(SYS.ManagerClass):
	ManagingValueClass=ChildClass

#Define
MyTeamer=SYS.TeamerClass(
		**{
			'TeamingClassesDict':{
				'MyChildren':ChildrenClass
			}
		}
	)['#map@set'](
		{
			'-MyChildren':{
				'|Aurelie':{
					'MyInt':0
				}
			}
		}
	)

#print
print('MyTeamer is ')
SYS._print(MyTeamer)


