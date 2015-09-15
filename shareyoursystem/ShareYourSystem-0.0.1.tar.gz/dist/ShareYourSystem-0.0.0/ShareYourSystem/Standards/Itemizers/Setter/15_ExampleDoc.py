
#ImportModules
import ShareYourSystem as SYS

#Define and set a dict
MySetter=SYS.SetterClass(
	).set(
		'set',
		{
			'#liarg':('MyRedirectStr','MyStr')
		}
	).set(
		'set',
		{
			'#liarg':'MyFirstStr',
			'#kwarg':{'SettingValueVariable':'SettingValueVariable'}
		}
	).set(
		'set',
		{
			'#liarg:#map@get':['MyRedirectStr','MyFirstStr'],
			#'#kwarg':{'SettingValueVariable':'salut'}
		}
	).set(
		'set',
		{
			'#liarg':['MyInt'],
			'#kwarg':{'SettingValueVariable':2}
		}
	).set(
		'set',
		{
			'#liarg':['MyThirdStr'],
			'#kwarg:#map@get:#key':{'MyFirstStr':'allo!'}
		}
	).set(
		'set',
		{
			'#liarg':['MyFourStr'],
			'#kwarg:#map@get:#value':{'SettingValueVariable':'MyStr'}
		}
	).set(
		'set',
		{
			'#liarg':['MyFifthStr'],
			'#kwarg:#map@get:#key:value':{'MyFirstStr':'MyFourStr'}
		}
	)

#print
print('MySetter is ')
SYS._print(MySetter)
