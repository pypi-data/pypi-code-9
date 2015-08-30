#-*-encoding:utf-8-*-
from smart_open import sopen
import re
def trim(inputFile, outputFile, lines):
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		for line in text:
			if not line:
				break
			if lines: #trim blank lines
				if not re.search('^$', line):
					output.write(line)
			
			else:
				line = line.strip()
				output.write(line+'\n')
				
