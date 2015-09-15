
#ImportModules
import ShareYourSystem as SYS
import numpy as np

# Number of samplepoints
N = 100
# sample spacing
T = 1.0 / 800.0
SampleFloatsArray = np.linspace(0.0, N*T, N)

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_ValueVariable=np.array(
			[
				0.5*np.sin(50.0 * 2.0*np.pi*SampleFloatsArray)+np.sin(80.0 * 2.0*np.pi*SampleFloatsArray),
				0.5*np.sin(50.0 * 2.0*np.pi*SampleFloatsArray+np.pi/3.),
				np.sin(80.0 * 2.0*np.pi*SampleFloatsArray)
			]
		),
		_SampleFloatsArray=SampleFloatsArray,
		_GlobalBool=True
	)

#plot
import matplotlib.pyplot as plt
plt.subplot(141)
plt.plot(
	SampleFloatsArray,
	MyNumscipyer.NumscipiedValueFloatsArray.T
)
plt.subplot(142)
plt.plot(
	MyNumscipyer.NumscipiedFourierFrequencyFloatsArray,
	MyNumscipyer.NumscipiedFourierAmplitudeFloatsArray.T
)
map(
	lambda __NumscipiedFourierMaxTupleFloat:
	plt.plot(
		*__NumscipiedFourierMaxTupleFloat,
		marker='o'
	),
	SYS.flat(MyNumscipyer.NumscipiedFourierMaxTupleFloatsArray)
)
plt.subplot(143)
plt.plot(
	MyNumscipyer.NumscipiedFourierFrequencyFloatsArray,
	MyNumscipyer.NumscipiedFourierPhaseFloatsArray.T
)
plt.subplot(144)
plt.plot(
	MyNumscipyer.NumscipiedFourierFrequencyFloatsArray,
	SYS.sum(MyNumscipyer.NumscipiedFourierCrossPhaseFloatsArray).T
)
plt.show()

