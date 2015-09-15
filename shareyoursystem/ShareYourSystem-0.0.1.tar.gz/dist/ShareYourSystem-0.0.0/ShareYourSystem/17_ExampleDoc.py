#ImportModules
import ShareYourSystem as SYS
import numpy as np

#get
InverseFunction=SYS.getInverseFunction(np.tanh)

#print
print(
	np.tanh(InverseFunction(0.1)),
	np.tanh(InverseFunction(1.)),
	np.tanh(InverseFunction(2.))
)
