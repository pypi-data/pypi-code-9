"""
    Test of mysql connector
"""

from swallow.inout.CSVio import CSVio
from multiprocessing import JoinableQueue

def test_basic():
    in_queue = JoinableQueue()

    for x in 'abcd':
        in_queue.put(['test',x])
    in_queue.put(None)

    csv_writer = CSVio()
    csv_writer.dequeue_and_store(in_queue,'test.csv')

