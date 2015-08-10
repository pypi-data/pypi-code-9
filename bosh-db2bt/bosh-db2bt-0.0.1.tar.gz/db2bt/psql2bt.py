import psycopg2
import requests
import timeit
import json
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

psql_datatype_map = {'INT': 'INT32', 'BOOLEAN': 'BOOL', 'TINYINT': 'INT8', 'SMALLINT':'INT16', 'MEDIUMINT':'INT32', 'INTEGER':'INT32','SERIAL':'INT32','BIGINT':'INT64','FLOAT':'FLOAT','REAL':'FLOAT','DOUBLE':'DOUBLE','DOUBLE PRECISION':'DOUBLE','DATE':'DATE32','DATETIME':'DATETIME32','CHAR':'STRING','VARCHAR':'STRING','BLOB':'VARSTRING','TEXT':'STRING','TINYBLOB':'STRING','TINYTEXT':'STRING','TIMESTAMP':'DATETIME32','TIME':'DATETIME32','CHARACTER VARYING':'STRING','CHARACTER':'STRING'};

def cmd2JSON(cmd):
   return json.dumps({'Stmt':cmd,'Workspace':"",'Opts':{}})

def getData(server,cmdStr):
	try:
		r = requests.post(server,data=cmd2JSON(cmdStr))
	except:
		print("BigObject server connection error : " + server)	
		return ""
	
	return json.dumps(r.json())


def psqlcopy(host_, port_, database_, user_, password_, table_ , server_ , option_flag_):

	if option_flag_  == 'APPEND' or option_flag_  == 'append':
		## ping server ?		
		ret = getData(server_ , "show tables " + table_ )
		if ret == "":
			return	
	else:
	## truncate case #############################################33
		ret = getData(server_ , "drop table " + table_ )
		if ret == "":
			return
	
		connect_str = "dbname='" + database_ + "' user='" + user_ + "' host='" + host_ + "' password='" + password_ + "' port='" + port_ + "'" 
		try:
			con = psycopg2.connect(connect_str)
		except psycopg2.Error as e:
			print(e)
			return
		except:
			print "Connect to the postgre database failed"
			return

		cursor = con.cursor()
		#cur.execute("select * from test")
		cursor.execute("SELECT column_name, data_type, ordinal_position FROM information_schema.columns WHERE table_name=\'" + table_ + "\' order by ordinal_position;" )

		row = cursor.fetchone()
		if row == None :
			print "empty table : " + table_
			return

		create_stmt = "CREATE TABLE " + table_ + " ( "
		col_count = 0
	#	for row in rows:
		while row is not None:
			#print (row)
			col_count = col_count + 1
			create_stmt += "'" + row[0] + "' "
			datatype = row[1].upper()

			if datatype.find('(') != -1:
				datatype = datatype.split('(')[0]

			if psql_datatype_map.has_key(datatype) == False :
				create_stmt += "VARSTRING , "
			else:
				create_stmt += psql_datatype_map[datatype]

			row = cursor.fetchone()
			#if col_count != len(rows):
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

	## truncate case #############################################33

	connect_str = "dbname='" + database_ + "' user='" + user_ + "' host='" + host_ + "' password='" + password_ + "' port='" + port_ + "'" 
	try:
		con = psycopg2.connect(connect_str)
	except psycopg2.Error as e:
		print(e)
		return
	except:
		print "Connect to the postgre database failed"
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


if __name__ == '__main__':
	start = timeit.default_timer()

	if len(sys.argv) < 9:
		print('psql2bt <host> <port> <db name> <user> <password> <table name> <bo host> <bo port> \nex. mysql2bt localhost 3306 test root 1234 sales localhost 9090')
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
	psqlcopy(db_srv, db_port, db_name, db_user, db_pass, db_table, bo_url, option_flag)
	end = timeit.default_timer()
	print("time : " + str(end - start))
	
