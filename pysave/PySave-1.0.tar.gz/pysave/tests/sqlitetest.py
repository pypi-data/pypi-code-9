from pysave import sqlite




if __name__ == "__main__":
    ''' Lets test it out '''
    sql = sqlite.sqlite("test.sqlite")
    sql.openconnection()
    sql.closeconnection()
    sql.sqlcommand('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')
    sql.sqlcommand("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")