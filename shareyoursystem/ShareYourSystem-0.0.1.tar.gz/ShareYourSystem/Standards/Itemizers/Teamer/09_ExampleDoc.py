
#ImportModules
import ShareYourSystem as SYS

#define
MyTeamDict=SYS.Teamer.TeamDict([('a',1),('b',2)])

#print
print('MyTeamDict is ')
SYS._print(MyTeamDict)

#get
print(MyTeamDict.getValue(0))
print(MyTeamDict.getValue(1))


