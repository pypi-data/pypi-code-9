
import os

class Log:
    "log file, which appends to the file rather than reading"

    def __init__(self, fn, mode='a', echo=False):
        self.fn = fn
        self.mode = mode
        self.echo = echo
        if 'w' in mode:
            f = self.open(mode=model)
            self.close(f)

    def write(self, string):
        f = self.open(mode=self.mode or 'a')
        f.write(string)
        f.close()
        if self.echo==True: 
            print(string,end='')

    def __call__(self, *args, sep=' ', end='\n'):
        f = self.open()
        print(*args, file=f, sep=sep, end=end)
        self.close(f)
        if self.echo==True: 
            print(*args, sep=sep, end=end)

    def open(self, fn=None):
        fn = fn or self.fn
        if fn is not None:
            if not os.path.exists(os.path.dirname(fn)):
                os.makedirs(os.path.dirname(fn))
            f = open(fn, self.mode or 'a')
        else:
            f = sys.stdout
        return f 

    def close(self, f):
        if f != sys.stdout:
            f.close()

    def delete(self):
        if os.path.exists(self.fn):
            os.remove(self.fn)

    def timestamp(self):
        # return a timestamp string for the current time
        from time import strftime
        return strftime("%Y-%m-%d %I:%M:%S %p")

