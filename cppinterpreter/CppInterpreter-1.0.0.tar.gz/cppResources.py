import subprocess

def runcmd(s1):
	return subprocess.call(s1, shell=True)

def isConditional(s1):
	'''Tests whether s1 is a conditional statement.'''
	if(s1[0:2]=='if'):
		return True
	elif(s1[0:4]=='else'):
		return True
	elif (' if ' in s1) or ('}if ' in s1) or (' if(' in s1) or ('}if(' in s1):
		return True
	elif (' else ' in s1) or ('}else ' in s1) or (' else{' in s1)\
	or ('}else{' in s1):
		return True
	else:
		return False

def editTempFile():
	'''runs nano on tempFile.cpp so that the head can be changed'''
	runcmd("nano tempFile.cpp")
	
def editStorage():
	'''runs nano on storage.cpp so that it can be directly changed.'''
	runcmd("nano storage.cpp")
	
def listCommands():
	print("Here are commands for this interpreter:")
	print("e: exit the interpreter")
	print("l: list commands")
	print("s: directly mofify storage.cpp")
	print("t: directly modify tempFile.cpp")
	
def checkCommand(s1):
	if s1=='l':
		listCommands()
	elif s1=='s':
		editStorage()
	elif s1=='t':
		editTempFile()
	else:
		pass
