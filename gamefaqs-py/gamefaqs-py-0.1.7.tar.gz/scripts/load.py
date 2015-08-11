import sqlite3


def load_script():
	# load data into sqlite database
	con = sqlite3.connect('gamefaqs.db')
	f = open('dump.sql', 'r')
	sql = f.read() 
	con.executescript(sql)
