import sqlite3
import os

here = os.path.dirname(__file__)

# load data into sqlite database
def load_data():
    with open(os.path.join(here, 'data', 'dump.sql'), 'r') as f:
        sql = f.read() 
		con.executescript(sql) 


