from pysave import mysql

"""
Please replace the username, password, server, and db name with ones that will work with yours

"""

if __name__ == "__main__":
    ''' Lets test it out '''
    test = mysql.mysql("test","Test12","localhost", "test")
    test.connect()
    test.sendinfo("CREATE TABLE MyGuests (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,email VARCHAR(50),reg_date TIMESTAMP)")
    test.close()

