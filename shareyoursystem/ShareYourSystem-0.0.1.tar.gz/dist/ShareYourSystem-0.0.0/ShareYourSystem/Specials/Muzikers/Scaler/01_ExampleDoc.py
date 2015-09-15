
#ImportModules
import ShareYourSystem as SYS
import os

#Definition a Scaler
MyScaler=SYS.ScalerClass().scale()

#write
import music21
MyScaler.write(
	music21.vexflow.fromObject(
		MyScaler.ScaledOrderedDict.values(
		)[60]['Streamer'].StreamedMusic21Variable,
		mode="html"
	),
	**{
		'FolderingPathVariable':'/Users/ledoux/Documents/MampLocalhost/vexflow/',
		'FilingKeyStr':"Scale.html"
	}
).close()
