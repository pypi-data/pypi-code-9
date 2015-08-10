__author__ = 'Feedah'


def display():
    print("Let play maximum value game")
    print("Enter The numbers to stat")


def add(val1, val2):
    return val1 + val2


def game():
    display()
    choice = raw_input("Do you want to play enter Y or N")

    while choice != 'n' and choice != 'N':
        if choice != 'Y':
            print 'wrong choice'
            choice = raw_input("Do you want to play enter Y or N")
        else:
            val1 = input("Enter the first Number")
            val2 = input("Enter the second Number")

            result = max(val1, val2)
            print("The result is = %d" % result)
            choice = raw_input("Do you want to play enter Y or N")
if __name__ == '__main__':
    game()