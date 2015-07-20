import threading
import datetime

from saltmill import Mill

def worker(tgt, num):
    """thread worker function"""
    mill = Mill()
    mill.login()
    print 'Start pinging {} , #{}, {}'.format(tgt, num, datetime.datetime.now().strftime('%H:%M:%S'))
    res = mill.local(tgt, 'test.sleep', '60')

    print 'Finish pinging {} , #{}, {}'.format(tgt, num, datetime.datetime.now().strftime('%H:%M:%S'))
    print '{} , #{} returns: {}'.format(tgt, num, str(res))

if __name__ == '__main__':
    threads = []
    for tgt in ['centest', 'test-149', 'mq01.meitun.pro', 'mq02.meitun.pro']:
        for num in range(1, 4):
            t = threading.Thread(target=worker,args=(tgt, num))
            threads.append(t)
            t.start()

