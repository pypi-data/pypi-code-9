
#ImportModules
import ShareYourSystem as SYS


#Explicit expression
MyPather=SYS.PatherClass(
	).set(
		'/ChildPather/GrandChildPather/MyInt',
		0
	)

#print
print("MyPather['/ChildPather/GrandChildPather/~] is ")
SYS._print(MyPather['/ChildPather/GrandChildPather/~'])

#print
print("MyPather['/ChildPather/GrandChildPather/..] is ")
SYS._print(MyPather['/ChildPather/GrandChildPather/..'])
