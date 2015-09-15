
#ImportModules
import ShareYourSystem as SYS

#Note that we can mute again a managed or teamed variable
class MakerClass(SYS.ManagerClass):pass

#get
MyParenter=SYS.ParenterClass(
	).set(
		'/-Views/|Run',
		{
			'MyInt':0
		}
	)

#mute
MyParenter['/-Views/!|Run']=MakerClass

#Define
MyParenter=SYS.ParenterClass(
	)['#map@set'](
		{
			'/-Views/-Run/-Panels/|Sensor':{
				'MyInt':0,
				'-Plots':{
					'MyStr':"hello"
				}
			}
		}
	)

#print
print('MyParenter is ')
SYS._print(MyParenter)