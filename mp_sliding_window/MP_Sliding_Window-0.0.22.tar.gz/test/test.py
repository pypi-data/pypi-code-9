from slidingwindow import SlidingWindow
import os,time, sys

size = 10
def generator(swindow):
    global size
    x = 0
    while x < 100:
        print swindow.name, swindow.get_running_tasks(), swindow.size
        if x % 9 == 0:
            print "RESIZING", size
            size += 1
        if x % 5 == 0:
            print "RESIZING", size
            size -= 1
        x += 1
        yield (x,)

def square(x):
    time.sleep(x%10)
    print x*x, os.getpid()



class MySlidingWindow(SlidingWindow):
    log_folder = 'logs'
    def __init__(self, name, *args, **kwargs):
        self.name = name
        super(MySlidingWindow,self).__init__(*args,**kwargs)

    def initializer(self,worker_id):
        if self.log_folder:
            sys.stderr = open('{}/worker_{}.stderr.log'.format(self.log_folder, worker_id),'a')
            sys.stdout = open('{}/worker_{}.stdout.log'.format(self.log_folder, worker_id),'a')

    def check_resize(sw):
         if sw.size != size:
            sw.resize(size)

sl = MySlidingWindow(name='A', size = 10, target=square, tasks = generator)

sl.start_async()
while sl.is_running():
    print "STILL RUNNING"
    time.sleep(3)