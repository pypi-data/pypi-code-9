#ImportModules
import ShareYourSystem as SYS

#define structure
MyParenter=SYS.ParenterClass(
	).command(
		'/-Children/|Erwan/-GrandChildren',
		('.../--^','#call:parent')
	)

#get faster the top parent
print("Get the top parent of MyParenter['/-Children/|Erwan/-GrandChildren'] gives ")
SYS._print(MyParenter['/-Children/|Erwan/-GrandChildren']['Top'])