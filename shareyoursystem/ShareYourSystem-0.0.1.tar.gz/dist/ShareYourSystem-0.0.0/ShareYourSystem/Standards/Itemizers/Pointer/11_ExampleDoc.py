
#ImportModules
import ShareYourSystem as SYS

#Point direct with a special Key str
MyPointer=SYS.PointerClass(
	).set(
		'-Children',
		{
			'|Aurelie':{},
			'|Erwan':{
				'ParentingTriggerVariable':[
					'->/^/|Aurelie'
				]
			}
		}
	)['?v']

#print
print('MyPointer is')
SYS._print(MyPointer)



