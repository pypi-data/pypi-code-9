#-*-encoding:utf-8-*-
from smart_open import sopen
import re
def contains(inputFile, outputFile, search, regex):
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		for line in text:
			if not line:
				break
			if regex and re.search(search, line) == None:
				output.write(line)
			elif not regex and search not in line:
				output.write(line)

def duplicatedLines(inputFile, outputFile, withoutBlankLines):
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		linesSeen = set()
		for line in text:
			if line not in linesSeen:
				output.write(line)
				if withoutBlankLines and line.strip()=='':
					pass
				else:
					linesSeen.add(line)
			
