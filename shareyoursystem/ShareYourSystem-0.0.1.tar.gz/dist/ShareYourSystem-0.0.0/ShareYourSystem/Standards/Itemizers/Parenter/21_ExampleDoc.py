#ImportModules
import ShareYourSystem as SYS

#define structure
MyParenter=SYS.ParenterClass(
	).get(
		'/-Children/|Aurelie/-GrandChildren/|Loup/?^'
	)

MyParenter.command(
		['TeamDict.values','ManagementDict.values'],
		[
			(
				'ParentingTriggerVariable',
				{'DeepInt':'#get:>>self[\'DeepInt\']+len(self.ParentedTotalPathStr.split("/"))'}
			),
			('setSwitch',['parent']),
			'#call:parent',
			('setSwitch',['parent']),
			'#call:parent',
		],
		_AfterWalkRigidBool=True,
		_BeforeSelfRigidBool=True
	)


#print
print('MyParenter is ')
SYS._print(MyParenter)

