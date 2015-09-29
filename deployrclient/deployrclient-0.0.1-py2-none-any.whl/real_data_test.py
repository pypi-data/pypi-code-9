
import json
import requests
from deployr_connection import DeployRConnection


# initialize
HOST = 'http://deployr.tidnode.cl:7400/deployr/'
deployr_connection = DeployRConnection(HOST)

# Login
print "*** Login ***"
deployr_connection.login("admin", "Gavilan0")

# Create project
print "*** Create project ***"
data = {'projectname': 'Andres', 'projectdescr': 'Andres'}
status_response, response = deployr_connection.call_api('r/project/create/', data)
project = response['deployr']['response']['project'];

# Upload files
print "*** Upload files ***"
_files = ['datos_meteorologicos.txt', 'Funciones_Analisis.R', 'Modelo_Alta_Radiacion.RData', 'Modelo_Baja_Radiacion.RData', 'Modelo_Centroides_Caida.RData', 'Modelo_Prob_caida.RData', 'set_completo.RData', 'set_datos_validos.RData']

for _file in _files:
	url_file ='/Users/andres/projects/agro/deployr_connection/files/' + _file

	file_content = open(url_file, 'rb').read()

	data = {'project': project['project'], 'filename': _file, 'descr': _file, 'overwrite': True}
	files = {'file': file_content}

	status_response, response = deployr_connection.call_api('r/project/directory/upload/', data, files=files)

# Execute script
print 'Execute script'
data = {'project': project['project'], 'filename': 'prediccion.R', 'directory': 'riego', 'author': 'admin'}
print data

deployr_connection.set_rinput("dias", "primitive", 2)
deployr_connection.set_rinput("lowerbound", "primitive", 70)
deployr_connection.set_rinput("upperbound", "primitive", 80)

deployr_connection.set_routput("prediccion_response")


status_response, response = deployr_connection.call_api('r/project/execute/script/', data)

print deployr_connection.r_inputs
print deployr_connection.r_outputs
