
#ImportModules
import ShareYourSystem as SYS

#Point direct with a special Key str
MyConnecter=SYS.ConnecterClass(
	).set(
		'-Children',
		{
			'|Aurelie':{},
			'|Erwan':{
				'ParentingTriggerVariable':{
					'connect':[
						'/^/|Aurelie',
						{'MyStr':"hello"},
						{'MyInt':0}
					]
				}
			}
		}
	)['?v']

#print
print('MyConnecter is')
SYS._print(MyConnecter)



