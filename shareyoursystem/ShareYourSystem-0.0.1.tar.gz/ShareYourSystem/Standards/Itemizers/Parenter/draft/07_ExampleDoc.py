
#ImportModules
import ShareYourSystem as SYS

#define and get two children
MyParenter=SYS.ParenterClass(
	).array(
		[
			['&Layers'],
			['$First','$Second'],
			['&Neurons'],
			['$E','$I']
		]
	).command(
		'+&.values+$.values',
		{
			'parent':[],
			'#bound:recruit':lambda _InstanceVariable:_InstanceVariable[
						'/Top/NeuronsDict'
					].__setitem__(
						_InstanceVariable.ManagementTagStr,
						_InstanceVariable
					) 
					if _InstanceVariable['/^/ParentKeyStr']=="Neurons"
					else None,
			#'/Top/NeuronsList.append':{
			#	'#set':[">>self"],
			#	'#if':[
			#		('/^/ParentKeyStr',SYS.operator.eq,"Neurons")
			#	]
			#}
		},
		_AfterWalkRigidBool=True
	)

#print
print('MyParenter.NeuronsList is ')
SYS._print(MyParenter.NeuronsList)

