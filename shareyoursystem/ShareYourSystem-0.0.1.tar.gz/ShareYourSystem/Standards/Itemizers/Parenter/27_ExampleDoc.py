#ImportModules
import ShareYourSystem as SYS

#define structure
MyParenter=SYS.ParenterClass(
	).set(
			'-Models',[	]
	).set(
			'-Views',[('MyInt',0),('ParentingTriggerVariable',33)]
		)

#print
#print(MyParenter.TeamDict['Models'])
#print(MyParenter.TeamDict['Views'])
#MyParenter.TeamDict['Models']
#MyParenter['-Models']
#MyParenter['/-Views']
#print(MyParenter['/-Models'].ParentingTriggerVariable)
#print(MyParenter['/-Views'].ParentingTriggerVariable)
#print(MyParenter.TeamDict['Models'].ParentingTriggerVariable)
#print(MyParenter.TeamDict['Views'].ParentingTriggerVariable)
