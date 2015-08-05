"""
This file contains the format protocol between parser and worker

Defines which variables the parser will send to the message queue and
respective index

Variables not found in request ( not specified in log format) will be empty

By default, only request with status 200 are parsed. To change,
see parser_functions.py


Domain can be a list of domains. 
Reason: In some nginx access log, there can be:
'server_name domain1 domain2'
Hence, the request could belong to either domain

IP can be a list of ips.
Reason: Internal + External IP

"""

message_array = [
	'domain', 
	'server_ip',
	'remote_addr',
	'time_local',
	'request',
	'status',
	'body_bytes_sent',
	'request_time'
]

message_array_map = {
	'domain' : 0,
	'server_ip' : 1,
	'remote_addr' : 2,
	'time_local' : 3,
	'request' : 4,
	'status' : 5,
	'bytes_sent' : 6,
	'request_time' : 7
}