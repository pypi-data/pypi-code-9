#ImportModules
import ShareYourSystem as SYS

#init
MyList=[
	[2,3],
	[3,4,[5,9]]
]

#print
print(SYS.sum(MyList))

#print
print(SYS.flat(MyList))

#array
MyArray=SYS.numpy.array(
	[
		[2,3],
		[3,4]
	]
)

#print
print(SYS.sum(MyArray))

#array
MyArray=SYS.numpy.array(
	[
		[[2,1],[3,5]],
		[[3],[4,66]]
	]
)

#print
print(SYS.sum(MyArray))

