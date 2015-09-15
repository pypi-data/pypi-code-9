
#ImportModules
import ShareYourSystem as SYS

#define and get two children
MyParenter=SYS.ParenterClass(
	).get(
		'/-Children/|Aurelie/-GrandChildren/|Loup'
	).get('?v')

#print
print('MyParenter is ')
SYS._print(MyParenter[
	'/-Children/|Aurelie/-GrandChildren/|Loup'
].ParentedTotalSingularTeamOrderedDict.keys())

