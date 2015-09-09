from multiprocessing import Queue, Pool, Manager, Process
import sys, os
from Queue import Empty



class SlidingWindow(object):


    def __init__(self, size, target, tasks):
        self._is_running= False
        self.run_async= False
        self.size = size
        self.target = target
        self.tasks = tasks(self)

        self.max_size = size
        self.slots = Queue()
        self.reduce_slots = Queue()
        for i in range(self.size):
            self.slots.put(i)

        self.running_tasks = Manager().list([])


    def check_resize(self):
        pass


    def initializer(self,token_id):
        pass


    def callback(self,*args,**kwargs):
        pass


    def get_running_tasks(self):
        return list(self.running_tasks)


    def cb_wrapper(self, task, token, pool):
        def new_func(*args,**kwargs):
            self.callback(*args,**kwargs)
            pool.close()
            self.running_tasks.remove(task)
            try:
                self.reduce_slots.get_nowait()
            except Empty:
                self.slots.put(token)  
        return new_func


    def start(self, running_tasks=None):
        self.run_async= False
        self._is_running = True
        if running_tasks:
            self.running_tasks = running_tasks
        for task in self.tasks:
            token = self.slots.get(block=True)
            self.running_tasks.append(task)
            try:
                pool = Pool(1, self.initializer, [token])
                pool.apply_async(self.target,task, callback=self.cb_wrapper(task, token, pool))
            except Exception as e:
                print e
            self.check_resize()

        for i in range(self.size):
            self.slots.get(block=True)
            
    def start_async(self):
        self.run_async= True
        self.process = Process(target=self.start,args = (self.running_tasks))
        self.process.start()


    def stop_async(self):
        if self.run_async and self.process and self.process.is_alive():
            self.process.terminate()

    def is_running(self):
        if self.run_async:
            return self.process.is_alive()
        else:
            return self.is_running

    def resize(self, new_size):
        diff = new_size - self.size
        self.size = new_size
        if diff > 0:
            for i in range(self.max_size, self.max_size + diff):
                self.slots.put(i)
            self.max_size += diff
        elif diff < 0:
            for i in range(-diff):
                try:
                    token = self.slots.get_nowait()
                except Empty:
                    self.reduce_slots.put(None)

