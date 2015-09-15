
#ImportModules
import ShareYourSystem as SYS

#define and get two children
MyManager=SYS.ManagerClass(
	)['#map@get']('/|First/-Things','/|First/-Stuffs','|Second')

MyManager['#each:|']=[
	{
		'MyStr':"I am the first"
	},
	{
		'MyStr':"I am the second"
	}
]

MyManager['#each:/|First/-']=[
	{
		'MyInt':0
	},
	{
		'MyStr':"hello"
	}
]

#print
print('MyManager is ')
SYS._print(MyManager)


