
#ImportModules
import ShareYourSystem as SYS

#Define
MyConditioner=SYS.ConditionerClass()
		
#map get
MyConditioner['#map@get'](
	'FirstChildConditioner',
	'SecondChildConditioner',
	'FirstChildItemizer'
)

#get with a filter on the __dict__ values
MyConditioner.get(
		{
			'#filter':
			[
				(type,SYS.operator.eq,SYS.ConditionerClass),
				('SetTagStr',str.startswith,'#direct:First'),
				SYS.GetClass(lambda self:'Child' in self['SetTagStr']),			
			],
			'#scan':'>>self.__dict__.values()'
		}
	)

#print
print('get only the FirstChildConditionner gives')
SYS._print(MyConditioner.GettedValueVariable)

#get with a filter on items in a dict
MyConditioner.set(
		'MyDict',
		{
			'FirstObject':object(),
			'SecondObject':object()
		}
	).get(
		{
			'#filter':
			[
				True		
			],
			'#scan':'>>self.MyDict.items()'
		}
	).set(
		'GettedValueVariable',
		'>>dict(self.GettedValueVariable).values()'
	)

#print
print('get all the objects gives')
SYS._print(MyConditioner.GettedValueVariable)

#filter again
MyConditioner.get(
		{
			'#filter':
			[
				(0,str.startswith,'First')		
			],
			'#scan':'>>self.MyDict.items()',
			'#modify':'>>dict(self.GettedValueVariable).values()'
		}
	)

#print
print('get just the first object gives')
SYS._print(MyConditioner.GettedValueVariable)