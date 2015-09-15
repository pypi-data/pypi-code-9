
#ImportModules
import ShareYourSystem as SYS

#array original
MyArrayer=SYS.ArrayerClass(
	).array(
		["AArrayer","BArrayer"],
		[{'MyStr':"hello"},{}]
	)

#Definition the AttestedStr
print('MyArrayer is ')
SYS._print(MyArrayer)

#array identical
MyArrayer=SYS.ArrayerClass(
	).array(
		["aArrayer","bArrayer"],
		{'MyInt':1}
	)

#Definition the AttestedStr
print('MyArrayer is ')
SYS._print(MyArrayer)


