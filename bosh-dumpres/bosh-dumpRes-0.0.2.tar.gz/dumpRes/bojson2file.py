# encoding=utf8  
import json
import sys
import csv

reload(sys)  
sys.setdefaultencoding('utf8')

#def json2xlsx(data_str , file_name):
#	import boshExcel
#	import os
#	data = json.loads(data_str)
#	result_table = data['Content']['content'];
#	template=file_name if os.path.exists(file_name) else None
#      	boshExcel.Default_output(result_table,template=template,output=file_name)

def json2xlsx(data_str , file_name):
	import boshExcel
	import os
	#template=file_name if os.path.exists(file_name) else None
      	boshExcel.Default_output(data_str,template=None,output=file_name)


def json2csv(data_str , output):
	#print(data_str , file_name, type(data_str) , type(file_name))
	data = json.loads(data_str)
	#print(data , type(data))
	count = 0
	if(type(data['Content']) != dict):
		print("no return table can be dumpped, admin statement?")
		print("data:\n" + str(data['Content']))
		return 0
	if 'content' in data['Content'].keys():
		for row in data['Content']['content']:
			output.writerow(row)
			count+=1
	else:
		print("no content can be dumpped, admin statement?")
		print("data:\n" + str(data['Content']))
		return 0

	#if file_name != "STDOUT":
		#print("insert " + str(count) + " rows")
	return count

if __name__ == "__main__":
	if len(sys.argv) < 2:	
		print('bojson2file <file type> <file name> \nex. bojson2file CSV test.csv')
		sys.exit(1)

	if sys.argv[2] != "":
		file_name = sys.argv[2]
	else:
		file_name = "STDOUT"

	if sys.argv[1] != "":
		file_type = sys.argv[1]
	else:
		file_type = "CSV"

	data = sys.stdin.readlines()
	if file_type == 'CSV':
		if file_name == "STDOUT":
			output = csv.writer(sys.stdout , quotechar='"', quoting=csv.QUOTE_ALL)	
		else:
			output = csv.writer(open(file_name, "w+") , quotechar='"', quoting=csv.QUOTE_ALL)

		total_count = 0 
		for jsonobj in data:
			count = json2csv(jsonobj,output)
			total_count += count
		if file_name != "STDOUT":
			print("dump rows : " + str(total_count) )


	elif file_type == 'XLSX':
		#print (file_name)
		if file_name == "STDOUT":
			print("please assign a file name")
			sys.exit(1)

		result_table = [];
		for jsonobj in data:
			data_part = json.loads(jsonobj)
			for row in data_part['Content']['content']:
				#print(type(row))
				result_table.append(row);
		json2xlsx(result_table,file_name)
