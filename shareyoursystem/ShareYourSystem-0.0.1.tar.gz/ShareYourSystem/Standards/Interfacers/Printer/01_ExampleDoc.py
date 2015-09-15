#ImportModules
import ShareYourSystem as SYS

#Define and print
MyPrinter=SYS.PrinterClass(
	)._print('hello')
	
#add some new stuff
MyPrinter.MyInt=0
MyPrinter.__class__.MyStr="hello"

#print itself
print('print itself gives')
print(MyPrinter)
