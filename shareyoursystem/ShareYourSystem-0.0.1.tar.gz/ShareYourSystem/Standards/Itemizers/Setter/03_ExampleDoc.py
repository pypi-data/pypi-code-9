#ImportModules
import ShareYourSystem as SYS

#Define and map set with a dict
MySetter=SYS.SetterClass()

#set with map set
MySetter['#map@set'](
		{
			'MyInt':0,
			'MyStr':"hello"
		}
	)

#map set with a tuples list
MySetter['#map@set'](
		[
			('MyFloat',2.),
			('MyBool',False)
		]
	)

#map set 
MySetter['#map@set']={
			'FirstObject':object(),
			'SecondObject':object()
		}

#Set a map set
MySetter.set(
		'#map@set',
		{
			'FirstInt':1,
			'SecondInt':2
		}
	)

#mapset a mapset
MySetter['#map@set'](
	[
		(
			'#map@set',
			{
				'FirstFloat':4.,
				'SecondFloat':5.
			}
		)
	]
)

#print
print('MySetter is ')
SYS._print(MySetter)
