 
import sqlite3 as lite
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(dir_path, 'szs.db')

class Database:
	def __init__(self):
		self.con = lite.connect(db_file)


	def select_tables(self):
		with self.con:
			cur = self.con.cursor()
			cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
			data = [x[0] for x in cur.fetchall()]
			return data

	def select_header(self, table):
		with self.con:
			cur = self.con.cursor()
			cur.execute('PRAGMA table_info('+table+')')
			data = [x[1] for x in cur.fetchall()]
			return data

	def select_row(self, table, row):
		with self.con:
			cur = self.con.cursor()
			cur.execute('SELECT * FROM '+table+' WHERE size=?', (row,))
			data = cur.fetchone()
			return data

	def select_col(self, table, col):
		with self.con:
			cur = self.con.cursor()
			cur.execute('SELECT '+col+' FROM '+table+'')
			data = [x[0] for x in cur.fetchall()]
			return data

	def select_row_dict(self, table, row):
		header = self.select_header(table)
		row = self.select_row(table, row)
		return dict(zip(header, row))

	def select_choices(self):
		tables = self.select_tables()
		choices = {}
		for table in tables:
			choices[table] = self.select_col(table, 'size')
		return choices
			



if __name__ == '__main__':
	cat = cat263()
	print('tables: {}'.format(Database().select_tables()))
	print('choices: {}'.format(Database().select_choices()))
	print('column from IPE: {}'.format(Database().select_col('IPE', 'size')))
	print(cat.mfd())
	print(cat.mvrd())






