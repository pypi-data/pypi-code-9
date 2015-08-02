#!/usr/bin/python
#
#author: Noah Rossignol
#version: 1.0.0
#date: 08/01/2015
#
#  Copyright 2015 Noah Rossignol
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  More information on the GNU General Public License at <http://www.gnu.org/licenses/>
#
#  To ask questions or give comments on how to improve the code, contact
#  me at noahrossignol@yahoo.com
#
import subprocess
import os
from cppResources import *

def compileCurrent():
	'''Compiles everything that has been entered.  If an error occurs,
	it will restore the file to a previous version that was correct.'''
	runcmd("touch tmp")
	
	#The main function has an open bracket, so it needs a closing bracket
	#before it can compile
	with open("tempFile.cpp",'a') as output:
		output.write('}')
	
	res=runcmd("g++ tempFile.cpp -o tempFile.o")
	if res!=0:
		#There was an error. I need to restore what was correct
		runcmd("rsync correct.cpp tempFile.cpp")
		runcmd("rsync cstorage.cpp storage.cpp")
	elif firstLine==True:
		runcmd("chmod +x tempFile.o")
		runcmd("./tempFile.o > tmp")
		firstLine==False
		
		#now the closing bracket is removed so that more commands can be
		#added to the main function
		with open("tempFile.cpp",'r+') as output:
			output.seek(-1,2)
			output.truncate()
	else:
		runcmd("./tempFile.o > tmp")
		
		#remove the closing bracket here too
		with open("tempFile.cpp",'r+') as output:
			output.seek(-1,2)
			output.truncate()
			
	with open('tmp','r') as infile:
		transcript.append(infile.read())
	if len(transcript) < 2:
		print(transcript[0])
	else:
		print(transcript[-1][len(transcript[-2]):])


cwd=os.getcwd()
head="#include <iostream>\n"
head+="#include <"+cwd+"/storage.cpp>\n"
head+="using namespace std;\n"
head+="int main(){\n"

print("\n")		
print("C++ Interpreter 1.0")
print("Noah Rossignol August 2015")
print("Enter 'e' to exit.")
print("Enter 'l' to list other commands")
print("---------------------------")
transcript=[]
firstLine=True
waiting=False
depth=0
runcmd("touch cstorage.cpp")
		
with open("tempFile.cpp",'w') as output:
	output.write(head)
	
with open("storage.cpp",'w') as output:
	output.write("#include <iostream>\n#include <string>\n")
	output.write("using namespace std;\n")

while(True):
	#up to now everything is correct, so I save a snapshot of the file
	if waiting==False:
		runcmd("rsync tempFile.cpp correct.cpp")
		runcmd("rsync storage.cpp cstorage.cpp")
	
	#read the new line
	if waiting==True:
		currentLine=raw_input("... : ")
	else:
		currentLine=raw_input("C++ : ")
	
	#see if user has asked to exit
	if currentLine=='e':
		runcmd("rm tempFile.*")
		runcmd("rm correct.cpp")
		runcmd("rm storage.cpp")
		runcmd("rm cstorage.cpp")
		runcmd("rm tmp")
		break
	
	#check for non-C++ commands
	elif currentLine in ['l','s','t']:
		checkCommand(currentLine)
	
	#make sure that this line is not part of a code block
	#if it is, do not just compile this line
	elif ("{" in currentLine) or (waiting == True):
		if waiting==False:
			#save a correct version of storage in case it needs to be restored
			conditional = isConditional(currentLine)
			if conditional:
				runcmd("rsync tempFile.cpp correct.cpp")
			else:
				runcmd("rsync storage.cpp cstorage.cpp")
		if(conditional):
			with open("tempFile.cpp",'a') as output:
				output.write(currentLine+'\n')
		else:
			with open("storage.cpp",'a') as output:
				output.write(currentLine+'\n')
		if "{" in currentLine:
			depth += 1
		if ("}" in currentLine) and (depth == 1):
			compileCurrent()
			depth -=1
			waiting=False
			conditional=False
		elif("}" in currentLine):
			depth -= 1
		else:
			waiting=True
	
	#if all is normal, append the line and compile the file
	else:
		with open("tempFile.cpp",'a') as output:
			output.write(currentLine+'\n')
		compileCurrent()
