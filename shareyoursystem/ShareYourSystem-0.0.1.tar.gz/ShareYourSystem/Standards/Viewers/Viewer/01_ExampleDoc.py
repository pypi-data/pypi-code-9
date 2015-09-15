
#ImportModules
import ShareYourSystem as SYS

#A Viewer alone is not so much good
LonelyViewer=SYS.ViewerClass(
	).view(
	)

#print
print('LonelyViewer is ')
SYS._print(LonelyViewer)

#Definition of a Controller instance and the Child Modeler automatically model
MyController=SYS.ControllerClass().set(
		'/-Views/|Table',
		{
		}
	)

#print
print('MyController is ')
SYS._print(MyController)


