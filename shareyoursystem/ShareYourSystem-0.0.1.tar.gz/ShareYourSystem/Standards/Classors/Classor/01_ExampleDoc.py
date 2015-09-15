#ImportModules
import ShareYourSystem as SYS
import json

#Definition a FooClass decorated by the ClassorClass
@SYS.ClassorClass()
class FooClass(object):
	pass

#print
print('FooClass.__dict__ is ')
print(
	json.dumps(
		dict(
			zip(
				FooClass.__dict__.keys(),
				map(
					str,
					FooClass.__dict__.values()
				)
			)
		),
		indent=2
	)
)