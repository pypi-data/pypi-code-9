from pysave import ini

user = "Test"
print(user)

if __name__ == "__main__":
    ''' Lets test it out '''
    i = ini.ini()
    i.putvar("test.ini", "TEST", "TestVar", user)
    user2 = i.getvar("test.ini", "TEST", "TestVar")
    print(user2)