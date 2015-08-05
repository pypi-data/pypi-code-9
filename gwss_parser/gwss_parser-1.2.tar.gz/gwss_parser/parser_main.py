import subprocess
import json
import time
import datetime
import re
import os
import threading

import redis

from config import *
from utils import jjoin
import parser_functions as PARSER
from parser_worker_format import message_array  # format contract
from functions import detect_all_config_file
from common.logger import log


def parse_log(row, pattern, server_ip):
	"""
	USE PARSER.PARSER_LIST to parse keys in row
	If any parse function returns none, discard the row
	:return: Parsed row
	"""

	try:
		res = pattern.match(row['line']).groupdict()
	except Exception, e:
		log.error(e, exc_info = True)
		log.error(row['line'])
		return None
		
	# custom parsing row begins
	for key, parse_function in PARSER.PARSER_LIST.iteritems():
		try:
			temp_res = parse_function(res[key])
			if temp_res is not None:
				res[key] = temp_res
			else:
				# parse function decides not to log this row
				return None
		except:
			# the row does not follow format expected by parser
			# or the parser is buggy. Ignore row at the moment
			return None

	# this part can't be changed at the moment
	res['domain'] = row['domain']
	res['server_ip'] = server_ip

	return res

	
def format_row(parsed_row):
	# return a formatted row according to the contract
	formatted_row = [parsed_row[x] if x in parsed_row else None for x in message_array]
	return formatted_row


def follow(LogAccess):
	"""Follow/Tail all files found in LogAccess"""
	last_ino = [os.stat(item['path']).st_ino if os.path.exists(item['path']) else None for item in LogAccess]

	f = [open(item['path'],'r') if os.path.exists(item['path']) else None for item in LogAccess]

	for the_file in f:
		if the_file:
			the_file.seek(0,2)

	n = len(f)

	'''
	Use a different method to tail multiple files 
	*Source: https://bitbucket.org/rushman/multitail
	*Reason: The previous method will cause lagging behind when there are
	different traffic levels between access log files because it will sleep when
	ONE file has no traffic
	*This version will sleep when ALL FILES has no traffic. This version works ONLY if
	log rotation happens in short period of time, all happens on all file together (which
	is usually the case).
	'''
	while True:
		# read every files, use server_name as key
		got_line = False
		for i in range(0, n):
			if f[i]:
				the_file = f[i]
				info = LogAccess[i]
				filePath = info['path']
				serverName = info['server_name']
				formatName = info['format_name']

				line = the_file.readline()
				if line:
					got_line = True
					yield {'domain': serverName, 'format': formatName, 'line': line}
				else:
					continue
			else:
				info = LogAccess[i]
				filePath = info['path']

				if os.path.exists(filePath):
					f[i] = open(filePath, 'r')
					last_ino[i] = os.stat(filePath).st_ino
				else:
					log.info("File %s doesn't exist !" % filePath)
					continue

		if not got_line:
			time.sleep(SLEEP)  # IF THERE IS NO TRAFFIC FROM ALL FILES
			for i in range(0, n):
				if f[i]:
					the_file = f[i]
					info = LogAccess[i]
					filePath = info['path']
					try:
						this_ino = os.stat(filePath).st_ino
					except:
						this_ino = 0
					if this_ino != last_ino[i]:
						the_file.close()
						while the_file.closed:
							try:
								f[i] = open(filePath,'r')
								the_file = f[i]
							except:
								pass
						last_ino[i] = os.stat(filePath).st_ino
				else:
					info = LogAccess[i]
					filePath = info['path']

					if os.path.exists(filePath):
						f[i] = open(filePath,'r')
						last_ino[i] = os.stat(filePath).st_ino
					else:
						log.info("File %s doesn't exist !" % (filePath))
						continue

def prepare_global_vars():
	global r, pipe
	global ssdb
	global last_call
	global log
	global RUN_PARSER

	r = redis.StrictRedis(REDIS_HOSTNAME)
	pipe = r.pipeline(transaction=False)  # no need for atomic
	
	last_call = datetime.datetime.now() 

	RUN_PARSER = True

def check_for_update(ListConfigFile):	
	try:
		global RUN_PARSER
		# check if nginx conf is correct
		proc = subprocess.Popen(["service nginx configtest"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate()

		if stdout.find("fail") == -1:
			need_restart = False
			current_time = int(datetime.datetime.now().strftime('%s'))

			# check last modified time of all files
			# if any files are modified within X seconds, restart
			for filePath in ListConfigFile:
				last_modified_time = int(os.stat(filePath).st_mtime)
				if (current_time - last_modified_time) < PARSER_UPDATE:
					# some file is modified between this update and last one
					need_restart = True
					break

			# rerun listing all config files
			# if there are new files, restart
			old_config_file = set(ListConfigFile)
			new_config_file = set(detect_all_config_file())
			diff = old_config_file.symmetric_difference(new_config_file)

			if diff:
				# there is some files added or removed
				need_restart = True

			if need_restart:
				log.debug("Parser needs restart soon")
				RUN_PARSER = False
			else:
				t = threading.Timer(PARSER_UPDATE, check_for_update, [ListConfigFile])
				t.daemon = True
				t.start()
		else:
			log.debug("Nginx conf fail, skip check update")
	except Exception, e:
		log.error(e, exc_info=True)

# -----------------Main function--------------------------

def run(server_ip, LogAccess, LogPattern, ListConfigFile):

	# prepare local variable
	redis_queue = list()
	rkey = jjoin(PREFIX, MESSAGE_QUEUE)  # redis queue key
	global RUN_PARSER

	try:
		prepare_global_vars()
		check_for_update(ListConfigFile)

		# short summary
		log.debug("======= ALL ACCESS FILES =======")
		log.debug(LogAccess)
		log.debug("Total access files: %d" % len(LogAccess))
		log.debug("================================")
		log.debug("Server IP: %s" % server_ip)
		log.debug("Tailing access files started...")
			
		countCheck = 0
		regexPattern = {}

		for key in LogPattern:
			regex_raw_pattern = LogPattern[key]
			regexPattern[key] = re.compile(regex_raw_pattern)

		global r
		global pipe

		source = follow(LogAccess)
		log.debug("PARSER runnning")
		while RUN_PARSER:
			# get next row and process, can be refactored more
			log.debug("before get line")
			row = source.next()

			# parse row
			log.debug("get line already")
					
			parsed_row = parse_log(row, regexPattern[row['format']], server_ip)
			log.debug("PARSER runnning")
			if parsed_row is None:
				# ignore this row
				continue

			formatted_row = None
			try:
				formatted_row = format_row(parsed_row)
			except Exception, e:
				log.error("Invalid row|Row %s|Parsed row %s|" % (row, parsed_row))
				continue

			if formatted_row is not None:
				redis_queue.append(json.dumps(formatted_row))
				# execute pipeline every second to save cpu
				current_time = datetime.datetime.now()
				global last_call
				if (current_time - last_call).seconds > 0:
					try:
						pipe.lpush(rkey, *redis_queue)
						pipe.execute()
						redis_queue[:] = []  # .clear function in python 3.3
						last_call = current_time
						log.info("Parse_success")
					except Exception, e:
						log.error(e, exc_info=True)
						log.error("Possible Redis connection problem")
					
		log.info("Parser stopped")							
	except Exception, e:
		# try except in outermost block !
		log.error(e, exc_info=True)
		log.error(row)

