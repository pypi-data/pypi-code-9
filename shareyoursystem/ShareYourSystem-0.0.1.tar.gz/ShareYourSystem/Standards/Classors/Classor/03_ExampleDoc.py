
#ImportModules
import ShareYourSystem as SYS

#Definition of a MakerClass decorated by a DoerClass instance
@SYS.ClassorClass()
class MakerClass(object):
	pass

#Definition of a derived BuilderClass decorated by a Deriver
@SYS.ClassorClass()
class BuilderClass(MakerClass):
	pass

#Print
#print('MakerClass.DerivedClassesList is '+str(MakerClass.DerivedClassesList))

#Definition the AttestedStr
print('MakerClass.DeriveClassesList is '+str(MakerClass.DeriveClassesList)) 

