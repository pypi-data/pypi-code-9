#!/usr/bin/env python
from minibus import MiniBusTwistedClient
from twisted.internet import task
# import pdb

class BasicTwistedPublisher(MiniBusTwistedClient):
    def __init__(self):
        MiniBusTwistedClient.__init__(self, name="BasicTwistedPublisher")
        self.pub = self.publisher("/chatter", {"type": "string"})
#         self.loop = task.LoopingCall(self.pub, "wub")
        self.loop = task.LoopingCall(self.send_a_msg)
        self.counter = 0

    def send_a_msg(self):
        print "sending a message"
        self.pub("wub %d" % self.counter)
        self.counter += 1

    def run(self):
        self.loop.start(1)  # Call once every second

if __name__ == "__main__":
#     pdb.set_trace()
    client = BasicTwistedPublisher()
    client.exec_()

