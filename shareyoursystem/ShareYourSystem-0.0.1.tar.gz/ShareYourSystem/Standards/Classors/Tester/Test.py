#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Classors import Tester
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Tester.TesterClass.__dict__.items()))

#Print a version of this object
_print(Tester.TesterClass())

#Print a version of his __dict__
_print(Tester.TesterClass().__dict__)

#Definition a module like a class and an attest function
AttestingFunctionStrsList=['attest_increment']
def attest_increment():
	Incrementer=IncrementerClass()
	Incrementer.increment()
	return Incrementer.IncrementingInt
@Tester.TesterClass()
class IncrementerClass():
	def default_init(self):
		self.IncrementingInt=0
	def increment(self):
		self.IncrementingInt+=1

#Attest and print the AttestedStr
attest()

#Check
#import os
#print(open(os.getcwd()+'/Attests/attest_increment.txt').read())

#And test
test()


