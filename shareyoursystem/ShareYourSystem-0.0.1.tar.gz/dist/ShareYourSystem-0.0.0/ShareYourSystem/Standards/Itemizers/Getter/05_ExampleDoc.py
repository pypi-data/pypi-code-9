
#ImportModules
import ShareYourSystem as SYS

#Definition a Getter
MyGetter=SYS.GetterClass()
MyGetter.MyInt=1
		
#print
print("MyGetter['MyFloat'] is ")
print(MyGetter['MyFloat'])
print('\n')

#print
print("MyGetter['MyInterfacer'] is ")
print(MyGetter['MyInterfacer'])
print('\n')

#print
print("MyGetter.get('MyStr',_NewBool=False).GettedValueVariable is ")
print(MyGetter.get('MyStr',_NewBool=False).GettedValueVariable)
print('\n')

#print
print('MyGetter is ')
SYS._print(MyGetter)


