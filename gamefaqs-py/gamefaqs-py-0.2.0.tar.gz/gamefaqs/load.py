import sqlite3

# load data into sqlite database
def load_data():
	con = sqlite3.connect('gamefaqs.db')
	f = open('data/dump.sql', 'r')
	sql = f.read() 
	con.executescript(sql)
