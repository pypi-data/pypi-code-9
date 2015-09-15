#ImportModules
import ShareYourSystem as SYS

#Attest the module
SYS.IncrementerClass().setAttest(
	SYS.AttesterClass.DeriveClassor.AttestingFolderPathStr
)

#Definition the AttestedStr
print(
'Attests file is written and is '+open(
	SYS.AttesterClass.DeriveClassor.AttestingFolderPathStr+'attest_increment.txt'
).read()
) 

