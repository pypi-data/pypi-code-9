
#ImportModules
import ShareYourSystem as SYS

#Point direct with a special Key str
MyConnecter=SYS.ConnecterClass(
	).set(
		'-Children',
		{
			'|Aurelie':{},
			'|Erwan':{}
		}
	)

MyConnecter[
		'/-Children/|Erwan'
	].connect(
		'/^/|Aurelie'
	)

#print
print('MyConnecter is')
SYS._print(MyConnecter)

