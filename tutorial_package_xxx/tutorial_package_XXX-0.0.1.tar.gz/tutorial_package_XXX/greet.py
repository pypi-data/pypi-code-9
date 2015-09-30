__author__ = 'uweschmitt'

def say_hello(who):
    print greeting(who)

def greeting(who):
    return "hi %s" % who

def main():
    say_hello("you")

if __name__ == "__main__":
    main()
