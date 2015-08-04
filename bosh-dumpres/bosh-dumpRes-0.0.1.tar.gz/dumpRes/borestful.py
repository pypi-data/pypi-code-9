import requests
import json
import sys

def cmd2JSON(cmd):
	return json.dumps({'Stmt':cmd,'Workspace':"",'Opts':{}})

def getData(server,cmdStr):
	r = requests.post(server,data=cmd2JSON(cmdStr) , stream=True)
	for content in json_stream(r.raw):
		#print(content)
		print (json.dumps(content))
	#r = requests.post(server,data=cmd2JSON(cmdStr))
	#return json.dumps(r.text)
	#return json.dumps(r.json())

def json_stream(fp):
	for line in fp:
		yield json.loads(line)

if __name__ == "__main__":
	server = sys.argv[1]
	cmd = sys.argv[2]
	getData(server,cmd)
