#-*-encoding:utf-8-*-
from smart_open import sopen
import re
def contains(inputFile, outputFile, search, regex):
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		for line in text:
			if not line:
				break
			if regex and re.search(search, line) != None:
				output.write(line)
			elif not regex and search in line:
				output.write(line)
