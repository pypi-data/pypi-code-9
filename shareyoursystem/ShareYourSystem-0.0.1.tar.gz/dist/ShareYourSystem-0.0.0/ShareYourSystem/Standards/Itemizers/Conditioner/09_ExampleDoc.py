
#ImportModules
import ShareYourSystem as SYS

#Define
MyConditioner=SYS.ConditionerClass()
MyConditioner.MyInt=1
		
#Condition that works
MyConditioner.set(
		"FirstStr",
		{
			'#value':"allo !",
			'#if':
			[
				('MyInt',SYS.operator.eq,1),
			]
		}
	)

#Condition that doesn't work
MyConditioner.set(
		"SecondStr",
		{
			'#value':"bonjour",
			'#if':
			[
				('MyInt',SYS.operator.eq,2),
			]
		}
	)

#print
print('MyConditioner is')
SYS._print(MyConditioner)

