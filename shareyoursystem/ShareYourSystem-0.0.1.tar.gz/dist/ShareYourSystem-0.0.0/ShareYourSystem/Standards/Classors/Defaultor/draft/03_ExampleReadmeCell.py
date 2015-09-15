import six,os
six.exec_(open(os.getcwd()+'/01_ExampleReadmeCell.py').read());

"""
#Definition the AttestedStr
SYS._attest(
	[
		'DefaultFoo.__dict__ is '+str(DefaultFoo.__dict__),
		'DefaultFoo.MyFloat is '+str(DefaultFoo.MyFloat),
		'DefaultFoo.MyList is '+str(DefaultFoo.MyList),
		'DefaultFoo.MyInt is '+str(DefaultFoo.MyInt),
		'',
		'SpecialFoo.__dict__ is '+str(SpecialFoo.__dict__),
		'SpecialFoo.MyFloat is '+str(SpecialFoo.MyFloat),
		'SpecialFoo.MyList is '+str(SpecialFoo.MyList),
		'DefaultFoo.MyInt is '+str(SpecialFoo.MyInt)
	]
) 

#Print

"""