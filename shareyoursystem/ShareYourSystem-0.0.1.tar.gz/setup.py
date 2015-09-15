"""


"""


#Definition Python Modules
from distutils.core import setup
from distutils.command.install import install
import os
import sys
import importlib

RequirePackageDict={
	#'inflect':'sudo pip install inflect',
	#'yaml':'sudo pip install pyyaml',
	#'pymongo':'sudo pip install pymongo',
	#'tables':'sudo pip install tables',
	#'brian2':'sudo pip install brian2'
}

#Define
class InstallClass(install):

	def run(self):

		#for
		for __RequirePackageModuleStr,__RequirePackagePipStr in RequirePackageDict.items():

			try:

				#import
				importlib.import_module(__RequirePackageModuleStr)
				
			except:

				#print
				print(__RequirePackageModuleStr+' is not installed...')
				print('... so we try to pip install it')

				#system
				os.system(__RequirePackagePipStr)

		#call the base method
		install.run(self)

#Execute a Setup
setup(

		#Author properties
		author='Erwan Ledoux',
		author_email='erwan.ledoux@ens.fr',

		#license

		#Application properties
		name='ShareYourSystem',
		version='0.0.1',
		url='http://shareyoursystem.ouvaton.org',

		#Commnd
		cmdclass={'install': InstallClass},

		#Packages properties
		packages=[
					'ShareYourSystem',
			 		'ShareYourSystem.Standards.Classors.Classor',
			 		'ShareYourSystem.Standards.Classors.Defaultor',
			 		'ShareYourSystem.Standards.Classors.Doer',
			 		'ShareYourSystem.Standards.Interfacers.Interfacer',
			 		'ShareYourSystem.Standards.Interfacers.Printer',
			 		'ShareYourSystem.Standards.Interfacers.Debugger',
			 		'ShareYourSystem.Standards.Classors.Propertiser',
			 		'ShareYourSystem.Standards.Tutorials.Incrementer',
			 		'ShareYourSystem.Standards.Classors.Attester',
			 		'ShareYourSystem.Standards.Tutorials.Decrementer',
			 		'ShareYourSystem.Standards.Classors.Tester',
			 		'ShareYourSystem.Standards.Classors.Observer',
			 		'ShareYourSystem.Standards.Classors.Binder',
			 		'ShareYourSystem.Standards.Classors.Watcher',
			 		'ShareYourSystem.Standards.Classors.Switcher',
			 		'ShareYourSystem.Standards.Classors.Mimicker',
			 		'ShareYourSystem.Standards.Classors.Classer',
			 		'ShareYourSystem.Standards.Itemizers.Itemizer',
			 		'ShareYourSystem.Standards.Itemizers.Getter',
			 		'ShareYourSystem.Standards.Itemizers.Setter',
			 		'ShareYourSystem.Standards.Itemizers.Executer',
			 		'ShareYourSystem.Standards.Itemizers.Conditioner',
			 		'ShareYourSystem.Standards.Itemizers.Arrayer',
			 		'ShareYourSystem.Standards.Itemizers.Pather',
			 		'ShareYourSystem.Standards.Itemizers.Commander',
			 		'ShareYourSystem.Standards.Itemizers.Teamer',
			 		'ShareYourSystem.Standards.Itemizers.Manager',
			 		'ShareYourSystem.Standards.Itemizers.Parenter',
			 		'ShareYourSystem.Standards.Itemizers.Connecter',
			 		'ShareYourSystem.Standards.Itemizers.Structurer',
			 		'ShareYourSystem.Standards.Itemizers.Coordinater',
			 		'ShareYourSystem.Standards.Itemizers.Explorer',
			 		'ShareYourSystem.Standards.Interfacers.Folderer',
			 		'ShareYourSystem.Standards.Interfacers.Filer',
			 		'ShareYourSystem.Standards.Interfacers.Processer',
			 		'ShareYourSystem.Standards.Interfacers.Numscipyer',
			 		'ShareYourSystem.Standards.Interfacers.Pymongoer',
			 		'ShareYourSystem.Standards.Interfacers.Hdformater',
			 		'ShareYourSystem.Standards.Guiders.Guider',
			 		'ShareYourSystem.Standards.Guiders.Scriptbooker',
			 		'ShareYourSystem.Standards.Guiders.Capturer',
			 		'ShareYourSystem.Standards.Guiders.Celler',
			 		'ShareYourSystem.Standards.Guiders.Notebooker',
			 		'ShareYourSystem.Standards.Guiders.Nbconverter',
			 		'ShareYourSystem.Standards.Guiders.Documenter',
			 		'ShareYourSystem.Standards.Modelers.Modeler',
			 		'ShareYourSystem.Standards.Modelers.Rower',
			 		'ShareYourSystem.Standards.Modelers.Inserter',
			 		'ShareYourSystem.Standards.Modelers.Retriever',
			 		'ShareYourSystem.Standards.Modelers.Findoer',
			 		'ShareYourSystem.Standards.Modelers.Merger',
			 		'ShareYourSystem.Standards.Modelers.Joiner',
			 		'ShareYourSystem.Standards.Viewers.Viewer',
			 		'ShareYourSystem.Standards.Viewers.Pyploter',
			 		'ShareYourSystem.Standards.Controllers.Controller',
			 		'ShareYourSystem.Standards.Controllers.Storer',
			 		'ShareYourSystem.Standards.Controllers.Drawer',
			 		'ShareYourSystem.Standards.Controllers.Shower',
			 		'ShareYourSystem.Standards.Controllers.Systemer',
			 		'ShareYourSystem.Standards.Recorders.Recorder',
			 		'ShareYourSystem.Standards.Recorders.Simulater',
			 		'ShareYourSystem.Standards.Recorders.Brianer',
			 		'ShareYourSystem.Standards.Recorders.Leaker',
			 		'ShareYourSystem.Specials.Lifers.Lifer',
			 		'ShareYourSystem.Specials.Lifers.Hopfer',
			 		'ShareYourSystem.Specials.Lifers.Stationarizer',
			 		'ShareYourSystem.Specials.Lifers.Stabilizer',
			 		'ShareYourSystem.Specials.Lifers.Transferer',
			 		'ShareYourSystem.Specials.Lifers.Oscillater',
			 		'ShareYourSystem.Specials.Predicters.Predicter',
			 		'ShareYourSystem.Specials.Oldpredicters.Oldpredicter',
			 		'ShareYourSystem.Specials.Oldpredicters.Predisenser',
			 		'ShareYourSystem.Specials.Oldpredicters.Prediploter',
			 		'ShareYourSystem.Specials.Oldpredicters.Predirater',
			 		'ShareYourSystem.Specials.Oldpredicters.Predispiker',
			 		'ShareYourSystem.Standards.Classors',
			 		'ShareYourSystem.Standards.Interfacers',
			 		'ShareYourSystem.Standards.Tutorials',
			 		'ShareYourSystem.Standards.Itemizers',
			 		'ShareYourSystem.Standards.Recorders',
			 		'ShareYourSystem.Standards.Controllers',
			 		'ShareYourSystem.Standards.Modelers',
			 		'ShareYourSystem.Standards.Viewers',
			 		'ShareYourSystem.Standards.Recorders',
			 		'ShareYourSystem.Standards.Guiders',
			 		'ShareYourSystem.Specials.Lifers',
			 		'ShareYourSystem.Specials.Predicters',
			 		'ShareYourSystem.Specials.Oldpredicters',
			 		'ShareYourSystem.Standards',
			 		'ShareYourSystem.Specials'
			 	]
			 ,

      	package_data={
          'ShareYourSystem':[
          		'Package.json'
          ],
          'ShareYourSystem.Specials.Lifers.Lifer':[
          	'_CIntegrateAndFireTransferFunction.so'
          ]
		},

    )

