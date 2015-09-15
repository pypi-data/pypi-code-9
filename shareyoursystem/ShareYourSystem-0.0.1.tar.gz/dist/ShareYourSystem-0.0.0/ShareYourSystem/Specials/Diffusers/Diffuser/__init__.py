# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Diffuser

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Systemer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
#</ImportSpecificModules>

#<DefineFunctions>
#</DefineFunctions>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
class DiffuserClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
							'DiffusingCoeffcientFloat',
							'DiffusingTauFloat'
						]

	def default_init(
						self,
						_DiffusingCoeffcientFloat=1.,
						_DiffusingTauFloat=1.,
						):
        
		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def computeDiffuserWithTimeInt(self,_TimeInt):

		#Print time
		print("Diffuser Index",_TimeInt)

		#Compute if during impulsion or relaxation
		if self.TimesList[_TimeInt] < TauFloat :
			GreenArray=(
				1.0-np.exp(-4.*DiffuserFloat*(np.pi*WaveFrequencyArray)**2*TimesList[_TimeInt])
				)/(4.0*DiffuserFloat*(np.pi*WaveFrequencyArray)**2)
			GreenArray[np.where(WaveFrequencyArray==0)]=TimesList[_TimeInt]
		else:
			GreenArray=(
				np.exp(
					-4.*(np.pi*WaveFrequencyArray)**2*DiffuserFloat*(TimesList[_TimeInt]-TauFloat))-np.exp(
					-4*(np.pi*WaveFrequencyArray)**2*DiffuserFloat*TimesList[_TimeInt])
					)/(4.0*DiffuserFloat*(np.pi*WaveFrequencyArray)**2
				)
			GreenArray[np.where(WaveFrequencyArray==0)]=TauFloat

		#Do Fourier Transform
		self.ConcentrationArray=(np.real(
			np.fft.ifftshift(
				np.fft.ifftn(
					np.fft.ifftshift(
						GreenArray*FourierSourceArray)
					)
				)
			)
		)

		#Record the Slices
		self.XySliceArray[_TimeInt,:,:]=self.ConcentrationArray[PlanesInt/2,:,:]
		self.XzSliceArray[_TimeInt,:,:]=self.ConcentrationArray[:,PixelsInt/2,:]	

	def do_diffuse(self):

		#Set an Alias for the Stimulation
		Stimulation=self['<Used>Stimulation']

		#Run Stimulation if not already
		if Stimulation.FourierSourceArray==None:
			if 1==1: 
				doProtocolWithTypeString("Stimulation")


		#Init the Variables Array
		w,u,v=(np.indices(
			(
				Stimulation.PlanesInt,Stimulation.PixelsInt,Stimulation.PixelsInt),dtype=np.float32
			)-Stimulation.PixelsInt/2.0)
		WaveFrequencyArray=np.float32(np.hypot(
							u/(Stimulation.PixelsInt*Stimulation.SpaceStepFloat),
							v/(Stimulation.PixelsInt*Stimulation.SpaceStepFloat),
							w/(Stimulation.PlanesInt*Stimulation.PlanesStepFloat))
							)
		del(w,u,v)
		self.TimesList=np.logspace(-1.0,1.0,StepTimesInt)*TauFloat
		self.ConcentrationArray=np.zeros((PlanesInt,PixelsInt,PixelsInt),dtype=np.float32)
		self.XySliceArray=np.zeros((Stimulation.PlanesInt,Stimulation.PixelsInt,Stimulation.PixelsInt),dtype=np.float32)
		self.XzSliceArray=np.zeros((Stimulation.PlanesInt,Stimulation.PixelsInt,Stimulation.PixelsInt),dtype=np.float32)
		self.MeansList=[0]*len(self.TimesList)
		self.DeviationsList=[0]*len(self.TimesList)

		#Compute Diffuser
		Pool.map(
			lambda TimeInt:
			self.computeDiffuserWithTimeInt(TimeInt),
			xrange(self.StepTimesInt)
			)

		#map(
		#	lambda TimeInt:
		#	computeDiffuserWithTimeInt(TimeInt),
		#	xrange(StepTimesInt)
		#	)
			
		#Compute Statistics
		ZDataArray=((self.ConcentrationArray[Stimulation.PlanesInt/2,:,:]**2)[
			np.where(Stimulation.TargetArray==1)
			]).reshape(-1)
		self.MeansList[TimeInt]=np.mean(ZDataArray)
		self.DeviationsList[TimeInt]=np.sqrt(np.var(ZDataArray))

	def record(self,_ScanH5pyFile,_CommitString):

		global ConcentrationArray,XySliceArray,XzSliceArray

		#DataDict
		DataDict={
					#MetaData Parameters
					'*StepTimesInt':self.StepTimesInt,
					'*DiffuserFloat':self.DiffuserFloat,
					'*TauFloat':self.TauFloat,

					#Analysis Data
					'&ConcentrationArray':self.ConcentrationArray,
					'&XySliceArray':self.XySliceArray,
					'&XzSliceArray':self.XzSliceArray
				}

		#Commit
		_ScanH5pyFile.commit(_CommitString,DataDict)

		#Print the Storer
		#print(_ScanH5pyFile)
		
		#Push
		_ScanH5pyFile.push()

	def plot(self):
		matplotlib.pyplot.figure(2)
		ax=matplotlib.pyplot.subplot(121)
		ax.plot(self.TimesList,array(self.MeansList),self.TimesList,array(self.DeviationsList))
		ax.grid('on')
		ax=matplotlib.pyplot.subplotsubplot(122)
		ax.plot(self.TimesList,array(self.DeviationsList)/array(self.MeansList))
		ax.grid('on')

	#</DefineMethods>
#</DefineClass>


