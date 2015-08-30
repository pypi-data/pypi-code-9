#-*-encoding:utf-8-*-
from smart_open import sopen
import re
import logging as log

def contains(inputFile, outputFile, search, regex):
	total = 0
	searched = 0
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		for line in text:
			total += 1
			if not line:
				break
			if regex and re.search(search, line) != None:
				output.write(line)
				searched+=1	
			elif not regex and search in line:
				output.write(line)
				searched+=1

	log.info('Total : %dsentences.' % total)
	log.info('Searched : %dsentences.(%d%%)' % ( searched, 100*(float(searched)/float(total)) ) )
