import mysql.connector
from mysql.connector import Error
import requests
import json
import sys
import timeit

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
			
			con = mysql.connector.connect(host=host_,
					port=port_,
					database=database_,
					user=user_,
					password=password_)

			if con.is_connected():
				print('Connected to MySQL database')
			else:
				print('Connected to MySQL database failed')
				return

			cursor = con.cursor()	

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
		except Error as e:
			print(e)
			return
		## truncate case ####################################	
	
	try:
		##get data	
		con = mysql.connector.connect(host=host_,
					port=port_,
					database=database_,
					user=user_,
					password=password_)

		if con.is_connected():
			print('Connected to MySQL database')
		else:
			print('Connected to MySQL database failed')
			return

		cursor = con.cursor()

		query = ("SELECT * FROM " + table_)
		cursor.execute(query)
		row = cursor.fetchone()	

		count = 0
		data_stmt = "("
 		while row is not None:	
			if data_stmt != "(":
				data_stmt += ",("				
			for data in row:
				data_stmt += "'" + unicode(data) + "',"
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


	except Error as e:
		print(e)

	
 
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
	if len(sys.argv) == 10:
		option_flag  = sys.argv[9]

	#print(db_srv ,db_port,db_name , db_user,db_pass, db_table, bo_srv )
	bo_url = "http://" + bo_srv + ":" + bo_port + "/cmd"
	mysqlcopy(db_srv, db_port, db_name, db_user, db_pass, db_table, bo_url , option_flag )
	end = timeit.default_timer()
	print("time : " + str(end - start))
