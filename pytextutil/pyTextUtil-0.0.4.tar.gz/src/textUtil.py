#-*-encoding:utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging as log
import datetime

def parseArgument():

	import argparse

	parser = argparse.ArgumentParser(description='Processing String.')

	#subparser
	subparser = parser.add_subparsers(dest='cmd')

	#subcommand list
        search = subparser.add_parser('search')
        search.add_argument('term', help='string to search.')
	search.add_argument('--regex', help='search with regex.', action='store_true')

        delete = subparser.add_parser('delete')
        delete.add_argument('term', help='string to delete.')
	delete.add_argument('--regex', help='search with regex.', action='store_true')
	delete.add_argument('--duplicatedLines', help='delete duplicated lines', action='store_true')
	delete.add_argument('--withoutBlankLines', help='duplicated test without blank lines', action='store_true')

	trim = subparser.add_parser('trim')
	trim.add_argument('--lines', help='trim blank lines.', action='store_true')

	#default arguments
	parser.add_argument('-i', '--input', help='file to process.')
	parser.add_argument('-o', '--output', help='file to save result.(default=stdout)') #smart_open.py
	parser.add_argument('-v', '--verbose', help='verbose mode. (0~1, 0:quiet, 1:verbose. default=0)', action='store_true')

	#parse!
	args = parser.parse_args()

	if not args.input:
		parser.error("No input file provided. use '-i' or '--input'")

	if args.verbose:
		log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
	return args
	
def main():
	start = datetime.datetime.now()
	args = parseArgument()

	#옵션에 따라 진행
	if args.cmd=='search':
		import search
		search.contains(args.input, args.output, args.term, args.regex)
	elif args.cmd=='delete':
		import delete
		if args.duplicatedLines:
			delete.duplicatedLines(args.input, args.output, args.withoutBlankLines)
		else:
			delete.contains(args.input, args.output, args.term, args.regex)
	elif args.cmd=='trim':
		from trim import trim
		trim(args.input, args.output, args.lines)

	took = datetime.datetime.now() - start
	
	log.info('Done! (%dsec.)' % (took.seconds))

if __name__=="__main__":
	main()
