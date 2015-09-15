
#ImportModules
import ShareYourSystem as SYS

#Define
MyConditioner=SYS.ConditionerClass(
	)['#map@set'](
		{
			'MyInt':0,
			'MyStr':"hello"	
		}
	)['#map@condition'](
		[
			(type,SYS.operator.eq,SYS.ConditionerClass),
			('MyInt',SYS.operator.eq,0),
			('MyStr',SYS.operator.eq,"#direct:hello")
		]
	)

#print
print('MyConditioner.ItemizedMapValueVariablesList is ')
print(MyConditioner.ItemizedMapValueVariablesList)