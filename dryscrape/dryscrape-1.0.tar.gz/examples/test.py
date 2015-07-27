from dryscrape import Session
from dryscrape.driver.webkit import Driver
from webkit_server import InvalidResponseError

import sys
link = sys.argv[1]
sess = Session(driver = Driver())
#sess.set_proxy("192.168.178.190", 9999)

if len(sys.argv) > 2:
  sess.set_error_tolerance(int(sys.argv[2]))

for i in range(2):
  sess.visit(link)
  sess.wait()
  sess.render("/tmp/test.png")
