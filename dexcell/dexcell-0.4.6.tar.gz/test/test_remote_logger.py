from dexma.dexcell import DexcellLoggingHandler
import logging
import time
import threading
import requests

class TestLogger(threading.Thread):
    def __init__(self,th_name, mac_number):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = th_name
        self.mac_number = mac_number


    def test_remote_logger(self):
        dict_seconds = dict()
        mac = 'mac-greenbox-%i' % self.mac_number
        config = '1c9004c6632e1bbbf2bd'
        remotelogger = logging.getLogger('%s-%s' % (mac, self.name))
        handler = DexcellLoggingHandler(mac, config)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        remotelogger.addHandler(handler)
        remotelogger.setLevel(logging.INFO)
        retry = 1
        while retry < 1000:
            t1 = time.time()
            remotelogger.info('Este test seguro que tarda, muy muy muy seguro')
            tfinal = time.time()-t1
            tfinalRound = round(tfinal, 1)
            if tfinalRound not in dict_seconds:
                dict_seconds[tfinalRound] = 0
            dict_seconds[tfinalRound] += 1
            #print 'time request for thread '+self.name +' is '+ str(retry) + ' is t= '+ str(tfinal)
            retry += 1
        print "for mac %s we have the next results" % mac
        keys = dict_seconds.keys()
        keys.sort()
        for key in keys:
            print key, dict_seconds[key]

    def run(self):
        self.test_remote_logger()


def test_one():
    th_list = []
    for j in range(1, 6):
        for i in range(2):
            th = TestLogger(i, j)
            th.start()
            th_list.append(th)

    while True:
        pass

def test_two():
    th_list = []
    for j in range(1, 6):
        for i in range(5):
            th = TestLogger(i, j)
            th.start()
            th_list.append(th)

    while True:
        pass

test_two()