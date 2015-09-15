
#ImportModules
import ShareYourSystem as SYS

#init
SYS.CommanderClass.CountInt=0
SYS.CommanderClass.GrabList=[]

#define and build a chain
MyCommander=SYS.CommanderClass(
	).array(
		[['ACommander','BCommander'],['1Commander','2Commander']],
		{'MyInt':'>>SYS.set(self.__class__,"CountInt",self.__class__.CountInt+1).CountInt'}
	).command(
		{
			'#filter':[(0,str.endswith,'Commander')],
			'#scan':'>>self.__dict__.items()',
			'#modify':'>>dict(self.GettedValueVariable).values()'
		},
		{
			'execute':{
				'#liarg':"self.__class__.GrabList.append(self.SetTagStr)",
				'#if':[
					('MyInt',SYS.operator.lt,3)
				]
			}
		},
		_AfterWalkRigidBool=True
	)

"""
#print
print('MyCommander is')
SYS._print(MyCommander)
"""

#print
print('MyCommander is GrabList')
SYS._print(MyCommander.GrabList)







