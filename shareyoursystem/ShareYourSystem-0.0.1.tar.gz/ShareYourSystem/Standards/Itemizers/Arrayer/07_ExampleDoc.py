
#ImportModules
import ShareYourSystem as SYS

#array original
MyArrayer=SYS.ArrayerClass(
	).array(
		[
			["AArrayer","BArrayer"],
			[
				'1Arrayer',
				{
					'#key':'2Arrayer',
					'#map@set':{'MyInt':2}
				}
			]
		]
	)

#Definition the AttestedStr
print('MyArrayer is ')
SYS._print(MyArrayer)

