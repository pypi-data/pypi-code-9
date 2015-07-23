from pysave import serialization

user = {'Player': 5, 'Speed': 7}
print(user)

if __name__ == "__main__":
    ''' Lets test it out '''
    ser = serialization.serialize()
    ser.savedata(user, 'testfile.txt')
    user2 = ser.loaddata('testfile.txt')
    print(user2)

