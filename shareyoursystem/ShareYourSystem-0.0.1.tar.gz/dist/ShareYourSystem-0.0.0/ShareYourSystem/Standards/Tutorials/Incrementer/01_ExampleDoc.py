
#ImportModules
import ShareYourSystem as SYS

from ShareYourSystem.Standards.Tutorials import Incrementer

#Definition an instance
MyIncrementer=SYS.IncrementerClass(
	).increment()
		
#Definition the AttestedStr
print('MyIncrementer is ')
SYS._print(MyIncrementer)

