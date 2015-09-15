
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
			'/Top/LayersDict.__setitem__':{
				'#set':["#get:ManagementTagStr",">>self"],
				'#if':[
					('/^/ParentKeyStr',SYS.operator.eq,"#direct:Layers")
				]
			}
		},
		_AfterWalkRigidBool=True
	)

#print
print('MyParenter.NeuronsDict.keys() is ')
SYS._print(MyParenter.NeuronsDict.keys())

#print
print('MyParenter.LayersDict.keys() is ')
SYS._print(MyParenter.LayersDict.keys())
