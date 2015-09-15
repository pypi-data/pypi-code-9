
#ImportModules
import ShareYourSystem as SYS

#Define
MyParenter=SYS.ParenterClass(
		**{
			'TeamingClassesDict':{
				'MyChildren':ChildrenClass,
				'YourChildren':ChildrenClass
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
print('MyParenter is ')
SYS._print(MyParenter)


