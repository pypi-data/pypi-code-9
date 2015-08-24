from saltmill import Mill

if __name__ == '__main__':
    mill = Mill()
    mill.login()

    print mill.local('test1', 'test.ping')
