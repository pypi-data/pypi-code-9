#-*-encoding:utf-8-*-
from smart_open import sopen
import re
import logging as log

def contains(inputFile, outputFile, search, regex):
	total = 0
	remained = 0
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		for line in text:
			total += 1
			if not line:
				break
			if regex and re.search(search, line) == None:
				output.write(line)
				remained += 1
			elif not regex and search not in line:
				output.write(line)
				remained += 1
	log.info('Total : %dsentences.' % total)
        log.info('Deleted : %dsentences.(%d%%)' % ( total-remained, 100*(float(total-remained)/float(total)) ) )

def duplicatedLines(inputFile, outputFile, withoutBlankLines):
	total = 0
	remained = 0
	with open(inputFile, 'r') as input, sopen(outputFile) as output:
		text = input.readlines()
		linesSeen = set()
		for line in text:
			total += 1
			if line not in linesSeen:
				output.write(line)
				remained += 1
				if withoutBlankLines and line.strip()=='':
					pass
				else:
					linesSeen.add(line)
			
	log.info('Total : %dsentences.' % total)
        log.info('Deleted : %dsentences.(%d%%)' % ( total-remained, 100*(float(total-remained)/float(total)) ) )
