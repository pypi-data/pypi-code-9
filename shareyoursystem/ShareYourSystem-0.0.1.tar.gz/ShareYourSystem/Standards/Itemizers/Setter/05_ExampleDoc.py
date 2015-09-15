#ImportModules
import ShareYourSystem as SYS
import collections

#Define and set child setters in a child dict
MySetter=SYS.SetterClass(
	)['set'](
		'MyOrderedDict',
		collections.OrderedDict(
			{
			'FirstSetter':SYS.SetterClass(),
			'SecondSetter':SYS.SetterClass()
			}
		)
	).set(
		'#each:MyOrderedDict',
		[
			{
				'MyStr':"hello",
				'MyInt':0
			},
			('MyFloat',5.)
		]
	)

#print
print('MySetter is ')
SYS._print(MySetter)
