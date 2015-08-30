#-*-encoding:utf-8-*-
from smart_open import sopen
import re
import logging as log

def trim(inputFile, outputFile, lines):
	total = 0
	notTrimmed = 0
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		for line in text:
			total += 1
			if not line:
				break
			if lines: #trim blank lines
				if not re.search('^$', line):
					output.write(line)
					notTrimmed+=1
			
			else:
				stripline = line.strip()
				output.write(stripline+'\n')
				if stripline == line[:-1]:
					notTrimmed+=1
	log.info('Total : %dsentences.' % total)
	log.info('Trimmed : %dsentences.(%d%%)' % (total-notTrimmed, 100*(float(total-notTrimmed)/float(total))))
