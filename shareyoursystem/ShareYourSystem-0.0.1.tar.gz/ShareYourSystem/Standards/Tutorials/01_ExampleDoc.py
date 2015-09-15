
#Define a Class
class CatClass(object):

	def __init__(self):

		self.MeowStr="meeeeoooow"

	def printMeow(self):

		print self.MeowStr

#Instance
LokiCat=CatClass()

#print
#print('LokiCat.printMeow() gives')
#LokiCat.printMeow()

#Define a Class
class BabyClass(object):

	def printMeow(self):

		print "arheu arheu arheu"

#Define
class KittyClass(CatClass,BabyClass):
	""" Kitty cats are cats but cute"""
	
	def printMeow(self):

		#print('My MeowStr is '+self.MeowStr)
		#self.__class__.__mro__[0]
		CatClass.printMeow(self)
		BabyClass.printMeow(self)
		#print 'And I am cute'

#Instance
LokiKitty=KittyClass()
print(LokiKitty.__class__.__mro__)

#Instance
print('\nLokiKitty.printMeow() gives')
LokiKitty.printMeow()


