
#ImportModules
import ShareYourSystem as SYS

#Definition and update with an exec Str
MyExecuter=SYS.ExecuterClass(
	).execute(
		'self.MySecondInt=1+1'
	)

#print
print('MyExecuter is ')
SYS._print(MyExecuter)
