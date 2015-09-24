import thread
import time

# Define a function for the thread
def print_time(thread_name, count):
   count = 0
   while count < 5:
      count += 1
      print "%s: %s" % ( "TEST", time.ctime(time.time()) )
   print thread_name
   print time.time()
   open('/tmp/vospace/durand/crds/config/hst/server_config','r').read()

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread 1", 2))
   thread.start_new_thread( print_time, ("Thread 2", 1))
except:
   print "Error: unable to start thread"

while 1: 
   pass
