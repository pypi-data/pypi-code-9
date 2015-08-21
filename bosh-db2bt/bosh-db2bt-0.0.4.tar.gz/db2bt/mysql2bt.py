import pymysql.cursors
import requests
import json
import sys
import timeit
import datetime

reload(sys)  
sys.setdefaultencoding('utf8')

mysql_datatype_map = {'INT': 'INT32', 'TINYINT': 'INT8', 'SMALLINT': 'INT16' , 'MEDIUMINT' : 'INT32', 'BIGINT' : 'INT64' ,'FLOAT' : 'FLOAT' , 'DOUBLE' : 'DOUBLE' , 'DATE' : 'DATE32', 'DATETIME':'DATETIME32', 'CHAR':'STRING', 'VARCHAR':'STRING','BLOB':'VARSTRING', 'TEXT':'STRING'};

def cmd2JSON(cmd):
   return json.dumps({'Stmt':cmd,'Workspace':"",'Opts':{}})

def getData(server,cmdStr):
	try:
		r = requests.post(server,data=cmd2JSON(cmdStr))
	except:
		print("BigObject server connection error : " + server)	
		return ""
	
	return json.dumps(r.json())


def mysqlload(host_, port_, database_, user_, password_, table_ , server_ , sql_stmt):
	## ping server ?		
	ret = getData(server_ , "show tables " )
	if ret == "":
		return
	try:
		##get data	
		con = pymysql.connect(host=host_,
					user=user_,
					password=password_,
					port=int(port_),
					db=database_,
					charset='utf8')
		with con.cursor() as cursor:
			cursor.execute(sql_stmt)
			row = cursor.fetchone()	

			count = 0
			data_stmt = "("
	 		while row is not None:	
				if data_stmt != "(":
					data_stmt += ",("				
				for data in row:
					if type(data) == datetime.datetime:				
						data = str(unicode(data))
					#elif type(data) != str:	
					#	data = str(data)
					data_stmt += json.dumps(data, ensure_ascii=False) + ","
					#data_stmt += "'" + unicode(data) + "',"
				data_stmt = data_stmt[:-1]
				data_stmt += ")"
				#print(data_stmt)
				count+=1			
				row = cursor.fetchone()

				if count != 0 and count % 1000 == 0:
					print("insert rows: " + str(count))
					insert_stmt = "INSERT INTO " + table_ + " VALUES" + data_stmt
					ret = getData(server_ , insert_stmt )
					if ret == "":
						return
					data_stmt = "("

			if data_stmt != "(":
				insert_stmt = "INSERT INTO " + table_ + " VALUES" + data_stmt 
				ret = getData(server_ , insert_stmt )
				if ret == "":
					return
				print("insert rows: " + str(count))
	
			cursor.close()

		con.close()


	except pymysql.MySQLError as e:
		print(e)
		return
	except:
		print("connect to mysql server failed : " + sys.exc_info()[0])
		return

def mysqlcopy(host_, port_, database_, user_, password_, table_ , server_ , option_flag_ ):

	if option_flag_  == 'APPEND' or option_flag_  == 'append':
		## ping server ?		
		ret = getData(server_ , "show tables " + table_ )
		if ret == "":
			return
		
	else:
		## truncate case ####################################
		ret = getData(server_ , "drop table " + table_ )
		if ret == "":
			return

		try:
			create_stmt = "CREATE TABLE " + table_ + " ( "

			con = pymysql.connect(host=host_,
					user=user_,
					password=password_,
					port=int(port_),
					db=database_,
					charset='utf8')
			with con.cursor() as cursor:
			
				query = ("DESC " + table_)
				cursor.execute(query)

				row = cursor.fetchone()	
		 		while row is not None:
					#print(row)
					create_stmt += "'" + row[0] + "' "
					datatype = row[1].upper()

					if datatype.find('(') != -1:
						datatype = datatype.split('(')[0]
						#print("type = ", datatype)

					if mysql_datatype_map.has_key(datatype) == False :
						create_stmt += "VARSTRING , "
					else:
						create_stmt += mysql_datatype_map[datatype]
			
					row = cursor.fetchone()

					if row != None:
						create_stmt += ", "

				create_stmt += " )"

				print("table truncated by : " + create_stmt)
				ret = getData(server_ , create_stmt )
				if ret == '{"Content": null, "Status": 0, "Err": ""}' :
					print("create done.")
				elif ret == "":
					return
				else:
					print(ret)
		except pymysql.MySQLError as e:
			print(e)
			return
		except:
			print("connect to mysql server failed : " + sys.exc_info()[0])
			return
		## truncate case ####################################	
	
	try:
		##get data	
		con = pymysql.connect(host=host_,
					user=user_,
					password=password_,
					port=int(port_),
					db=database_,
					charset='utf8')
		with con.cursor() as cursor:

			query = "SELECT * FROM " + table_
			cursor.execute(query)
			row = cursor.fetchone()	

			count = 0
			data_stmt = "("
	 		while row is not None:	
				if data_stmt != "(":
					data_stmt += ",("				
				for data in row:
					#print(data, type(data))	
					
					if type(data) == datetime.datetime:				
						data = str(unicode(data))
					#elif type(data) != str:	
					#	data = str(data)
					data_stmt += json.dumps(data, ensure_ascii=False) + ","
					
					
					#data_stmt += "'" + unicode(data) + "',"
					#if type(data) == unicode:
					#	data_stmt += "'" + data.encode('utf8','replace') + "',"
					#else:
					#	data_stmt += "'" + unicode(data) + "',"
				data_stmt = data_stmt[:-1]
				data_stmt += ")"
				#print(data_stmt)
				count+=1			
				row = cursor.fetchone()

				if count != 0 and count % 1000 == 0:
					print("insert rows: " + str(count))
					insert_stmt = "INSERT INTO " + table_ + " VALUES" + data_stmt
					#print(insert_stmt)
					ret = getData(server_ , insert_stmt )
					if ret == "":
						return
					data_stmt = "("

			if data_stmt != "(":
				insert_stmt = "INSERT INTO " + table_ + " VALUES" + data_stmt 
				ret = getData(server_ , insert_stmt )
				if ret == "":
					return
				print("insert rows: " + str(count))
		
			cursor.close()

		con.close()


	except pymysql.MySQLError as e:
		print(e)
		return
	except:
		print("connect to mysql server failed : " + str(sys.exc_info()[0]) )
		return

 
if __name__ == '__main__':
	start = timeit.default_timer()

	if len(sys.argv) < 9:
		print('mysql2bt <host> <port> <db name> <user> <password> <table name> <bo host> <bo port> \nex. mysql2bt localhost 3306 test root 1234 sales localhost 9090')
		sys.exit(1)
	#print(sys.argv)
	db_srv = sys.argv[1]
	db_port = sys.argv[2]
	db_name = sys.argv[3] 
	db_user = sys.argv[4]
	db_pass = sys.argv[5]
	db_table = sys.argv[6]
	bo_srv = sys.argv[7]
	bo_port = sys.argv[8]
	
	option_flag = "CREATE"
	if len(sys.argv) >= 10:
		option_flag = sys.argv[9]

	load_stmt = ""
	if len(sys.argv) == 11:
		load_stmt = sys.argv[10]

	#print(db_srv ,db_port,db_name , db_user,db_pass, db_table, bo_srv )
	bo_url = "http://" + bo_srv + ":" + bo_port + "/cmd"
	if load_stmt != "" and (option_flag == "LOAD" or option_flag == "load"):
		mysqlload(db_srv, db_port, db_name, db_user, db_pass, db_table , bo_url , load_stmt )
	else:
		mysqlcopy(db_srv, db_port, db_name, db_user, db_pass, db_table, bo_url , option_flag )
	end = timeit.default_timer()
	print("time : " + str(end - start))
