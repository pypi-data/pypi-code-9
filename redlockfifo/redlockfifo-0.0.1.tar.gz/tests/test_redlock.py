import threading
from time import sleep
import unittest
import fakeredis

from mock import patch
import redis
from redlock import Redlock, Lock
from fakeredis import FakeRedis


class FakeRedisCustom(FakeRedis):
    def __init__(self, db=0, charset='utf-8', errors='strict', **kwargs):
        self.fail_on_communicate = False
        if 'host' in kwargs and kwargs['host'].endswith('.inactive'):
            self.fail_on_communicate = True

        super(FakeRedisCustom, self).__init__(db, charset, errors, **kwargs)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        if self.fail_on_communicate:
            raise redis.exceptions.ConnectionError

        return super(FakeRedisCustom, self).set(name, value, ex, px, nx, xx)

    def eval(self, script, nb_of_args, *args):
        if self.fail_on_communicate:
            raise redis.exceptions.ConnectionError

        if script == Redlock.unlock_script:
            if self.get(args[0]) == args[1]:
                return self.delete(args[0])
            else:
                return 0


class RedlockTest(unittest.TestCase):

    @patch('redis.StrictRedis', new=FakeRedisCustom)
    def setUp(self):
        self.redlock = Redlock(get_servers_pool(active=1, inactive=0))
        self.redlock_with_51_servers_up_49_down = Redlock(get_servers_pool(active=51, inactive=49))
        self.redlock_with_50_servers_up_50_down = Redlock(get_servers_pool(active=50, inactive=50))

    def tearDown(self):
        fakeredis.DATABASES = {}

    def test_bad_connection_info(self):
        with self.assertRaises(Warning):
            Redlock([{"cat": "hog"}])

    def test_should_be_able_to_lock_a_resource_after_it_has_been_unlocked(self):
        lock = self.redlock.lock("pants", 10)
        self.assertIsInstance(lock, Lock)
        self.redlock.unlock(lock)
        lock = self.redlock.lock("pants", 10)
        self.assertIsInstance(lock, Lock)

    def test_safety_property_mutual_exclusion(self):
        """
            At any given moment, only one client can hold a lock.
        """
        lock = self.redlock.lock("pants", 100000)
        self.assertIsInstance(lock, Lock)
        bad = self.redlock.lock("pants", 10)
        self.assertFalse(bad)

    def test_liveness_property_A_deadlocks_free(self):
        """
            Eventually it is always possible to acquire a lock,
            even if the client that locked a resource crashed or gets partitioned.
        """
        lock_A = self.redlock_with_51_servers_up_49_down.lock("pants", 500)
        self.assertIsInstance(lock_A, Lock)
        sleep(1)
        lock_B = self.redlock_with_51_servers_up_49_down.lock("pants", 1000)
        self.assertIsInstance(lock_B, Lock)

    def test_liveness_property_B_fault_tolerance(self):
        """
            As long as the majority of Redis nodes are up, clients are able to acquire and release locks.
        """
        lock_with_majority = self.redlock_with_51_servers_up_49_down.lock("pants", 100000)
        self.assertIsInstance(lock_with_majority, Lock)

        lock_without_majority = self.redlock_with_50_servers_up_50_down.lock("pants", 100000)
        self.assertEqual(lock_without_majority, False)

    def test_locks_are_released_when_majority_is_not_reached(self):
        """
            [...] clients that fail to acquire the majority of locks,
            to release the (partially) acquired locks ASAP [...]
        """
        lock = self.redlock_with_50_servers_up_50_down.lock("pants", 10000)
        self.assertEqual(lock, False)

        for server in self.redlock_with_50_servers_up_50_down.servers:
            self.assertEqual(server.get('pants'), None)

    def test_avoid_removing_locks_created_by_other_clients(self):
        """
            [...] avoid removing a lock that was created by another client.
        """
        lock_A = self.redlock.lock("pants", 100000)
        self.assertIsInstance(lock_A, Lock)

        lock_B = Lock(validity=9000, resource='pants', key='abcde')
        self.redlock.unlock(lock_B)

        for server in self.redlock.servers:
            self.assertEqual(server.get('pants'), lock_A.key)

    def test_two_at_the_same_time_only_one_gets_it(self):
        threads = []
        threads_that_got_the_lock = []

        def get_lock_and_register(thread_name, redlock, resource, output):
            lock = redlock.lock(resource, 100000)
            if lock:
                output.append(thread_name)

        for i in range(2):
            thread = threading.Thread(
                target=get_lock_and_register, args=(i, self.redlock, 'pants', threads_that_got_the_lock)
            )
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        self.assertEqual(len(threads_that_got_the_lock), 1)


def get_servers_pool(active, inactive):
    redis_servers = []

    for i in range(inactive):
        server_name = "server%s.inactive" % i
        redis_servers.append({"host": server_name, "port": 6379, 'db': server_name})

    for i in range(active):
        server_name = "server%s.active" % i
        redis_servers.append({"host": server_name, "port": 6379, 'db': server_name})

    return redis_servers
