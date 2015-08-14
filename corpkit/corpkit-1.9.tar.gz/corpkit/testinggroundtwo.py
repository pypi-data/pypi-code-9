import Tkinter
from Tkinter import *
import threading
import Queue
import time

def thread(q, stop_event):
  """q is a Queue object, stop_event is an Event.
  stop_event from http://stackoverflow.com/questions/6524459/stopping-a-thread-python
  """
  while(not stop_event.is_set()):
    if q.empty():
      q.put(time.strftime('%H:%M:%S'))

class App(object):

  def __init__(self):
    self.root = Tk()
    self.win = Tkinter.Text(self.root, undo=True, width=10, height=1)
    self.win.pack(side='left')

    self.queue = Queue.Queue(maxsize=1)
    self.poll_thread_stop_event = threading.Event()
    self.poll_thread = threading.Thread(target=thread, name='Thread', args=(self.queue,self.poll_thread_stop_event))
    self.poll_thread.start()

    self.poll_interval = 250
    self.poll()

    self.root.wm_protocol("WM_DELETE_WINDOW", self.cleanup_on_exit)

  def cleanup_on_exit(self):
    """Needed to shutdown the polling thread."""
    print 'Window closed. Cleaning up and quitting'
    self.poll_thread_stop_event.set()
    self.root.quit() #Allow the rest of the quit process to continue


  def poll(self):
    if self.queue.qsize():
      self.selected_files = self.queue.get()
      self.win.delete(1.0,Tkinter.END)
      self.win.insert(Tkinter.END, self.selected_files)
    self._poll_job_id = self.root.after(self.poll_interval, self.poll)

app = App()
app.root.mainloop()