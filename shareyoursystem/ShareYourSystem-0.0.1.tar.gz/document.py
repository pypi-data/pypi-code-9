
#ImportModules
import ShareYourSystem as SYS

#Definition an Documenter instance
MyDocumenter=SYS.DocumenterClass(
	**{
		'DocumentingSubReadmeBool':True,
		'DocumentingConceptReadmeBool':False,
		'DocumentingConceptLibraryBool':False,
		'DocumentingDocumentBool':False,
		'DocumentingConceptSlideBool':False
	}
)

#map
map(
	MyDocumenter.document,
	[
		'Classors',
		#'Guiders',
		#'Interfacers',
		#'Itemizers',
		#'Modelers',
		#'Viewers',
		#'Simulaters',
		#'Ploters',
		#'Tutorials',
		#'Muzikers',
		
	]
)