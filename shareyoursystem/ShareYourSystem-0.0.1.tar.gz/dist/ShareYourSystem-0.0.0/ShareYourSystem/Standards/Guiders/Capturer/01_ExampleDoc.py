#ImportModules
import ShareYourSystem as SYS

#Definition a Capturer
MyCapturer=SYS.CapturerClass(
	).capture(
	)
print('Hello !')
print('Bonjour !')
MyCapturer.CapturingStopBool=True
print('Y a quelqu un?')

#Definition the AttestedStr
print('MyCapturer is ')
SYS._print(MyCapturer)




