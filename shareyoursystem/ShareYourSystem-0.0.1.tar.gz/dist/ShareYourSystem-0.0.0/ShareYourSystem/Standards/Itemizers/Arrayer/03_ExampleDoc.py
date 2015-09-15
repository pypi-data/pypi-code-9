
#ImportModules
import ShareYourSystem as SYS

#array
MyArrayer=SYS.ArrayerClass(
	).array(
		[
			["AArrayer","BArrayer"],
			["1Arrayer","2Arrayer"],
			["aArrayer"]
		],
		{
			'MyStr':"bonjour"
		}
	)

#print
print('MyArrayer is ')
SYS._print(MyArrayer)

#array
MyArrayer=SYS.ArrayerClass(
	).array(
		[
			["AArrayer","BArrayer"],
			["1Arrayer","2Arrayer"],
			["aArrayer","bArrayer"]
		],
		[
			#Special set for the AArrayers, nothing for the BArrayers
			[{'MyStr':"hello"},{}],
			#All the 1Arrayers,2Arrayers receive this setting
			{'MyInt':0},
			#nothing special for all the a and b arrayers
			{}
		],
	)

#print
print('MyArrayer is ')
SYS._print(MyArrayer)

