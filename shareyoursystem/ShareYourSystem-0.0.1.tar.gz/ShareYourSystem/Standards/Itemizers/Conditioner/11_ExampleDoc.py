
#ImportModules
import ShareYourSystem as SYS

#Define
MyConditioner=SYS.ConditionerClass(
	).get(
		'MyList'
	).set(
		'MyList.append',
		{
			'#value':4,
			'#if':[
				(type,SYS.operator.eq,SYS.ConditionerClass)
			]
		}
	)

#print
print('MyConditioner is')
SYS._print(MyConditioner)

