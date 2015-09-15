
#ImportModules
import ShareYourSystem as SYS

#Point direct with a special Key str
MyPointer=SYS.PointerClass(
	).set(
		'-Children',
		{
			'|Aurelie':{},
			'|Erwan':{
				'ParentingTriggerVariable':{
					'point':[
						'/^/|Aurelie',
						{'MyStr':"hello"},
						{'MyInt':0}
					]
				}
			}
		}
	)['?v']

#print
print('MyPointer is')
SYS._print(MyPointer)



