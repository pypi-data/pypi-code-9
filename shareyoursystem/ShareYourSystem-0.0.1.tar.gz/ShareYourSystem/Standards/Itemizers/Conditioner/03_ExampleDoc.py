#ImportModules
import ShareYourSystem as SYS

#Define and condition
MyConditioner=SYS.ConditionerClass(
			).condition(
				#ConditioningTestGetVariable
				'MyInt',
				#ConditioningGetBoolFunction
				lambda _TestVariable,_AttestVariable:_TestVariable==_AttestVariable,
				#ConditioningAttestGetVariable
				2,
				#ConditioningInstanceVariable
				#{'MyInt':3}
			)

#print
print('MyConditioner is ')
SYS._print(MyConditioner)

#condition ... it is going to try to get 2 in the dict 
#and raise an error but then use 2 
#as the self.ConditioningTestGetVariable
print('MyConditioner.condition(2) is ')
SYS._print(MyConditioner.condition(2))

#print
print('MyConditioner.condition(type,_AttestGetVariable=dict) is ')
SYS._print(MyConditioner.condition(type,_AttestGetVariable=dict))