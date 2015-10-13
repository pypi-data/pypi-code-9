import time
import unittest

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, TimeoutError

from await import threads, processes

DELAY = 0.5
TIMEOUT = 0.1
N = 2


class ThreadsTestCase(unittest.TestCase):

    def test_threads_decorator(self):

        def slow_add(x, y):
            time.sleep(DELAY)
            return x + y

        @threads(N)
        def async_add(x, y):
            time.sleep(DELAY)
            return x + y

        x, y = 2, 2

        start = time.time()

        results = []
        for i in range(N):
            results.append(async_add(x, y))

        checkpoint = time.time()

        results = [result.await() for result in results]

        end = time.time()
        assert (checkpoint - start) < DELAY
        assert DELAY < (end - start) < (DELAY * N)


    def test_shared_executor(self):

        executor = ThreadPoolExecutor(N)

        @threads(executor)
        def f(x):
            time.sleep(DELAY)
            return x

        @threads(executor)
        def g(x):
            time.sleep(DELAY)
            return 2*x

        start = time.time()

        results = []
        for i in range(N):
            results.append((f(i), g(i)))

        results = [
            (f_out.await(), g_out.await()) for f_out, g_out in results
        ]

        end = time.time()
        assert (N * DELAY) < (end - start) < (2 * N * DELAY)


    def test_timeout(self):

        @threads(N, timeout=TIMEOUT)
        def raises_timeout_error():
            time.sleep(DELAY)

        with self.assertRaises(TimeoutError):
            raises_timeout_error().await()

        @threads(N, timeout=2*DELAY)
        def no_timeout_error():
            time.sleep(DELAY)

        no_timeout_error().await()


    def test_future_function(self):

        @threads(N)
        def returns_function():
            def f():
                return True
            return f

        true = returns_function().await()
        assert true()


class ProcessesTestCase(unittest.TestCase):

    def test_processes_decorator(self):

        def slow_add(x, y):
            time.sleep(DELAY)
            return x + y

        @processes(N)
        def async_add(x, y):
            time.sleep(DELAY)
            return x + y

        x, y = 2, 2

        start = time.time()

        results = []
        for i in range(N):
            results.append(async_add(x, y))

        checkpoint = time.time()

        results = [result.await() for result in results]

        end = time.time()
        assert (checkpoint - start) < DELAY
        assert DELAY < (end - start) < (DELAY * N)


    def test_shared_executor(self):

        executor = ProcessPoolExecutor(N)

        @processes(executor)
        def f(x):
            time.sleep(DELAY)
            return x

        @processes(executor)
        def g(x):
            time.sleep(DELAY)
            return 2*x

        start = time.time()

        results = []
        for i in range(N):
            results.append((f(i), g(i)))

        results = [
            (f_out.await(), g_out.await()) for f_out, g_out in results
        ]

        end = time.time()
        assert (N * DELAY) < (end - start) < (2 * N * DELAY)


    def test_timeout(self):

        @processes(N, timeout=TIMEOUT)
        def raises_timeout_error():
            time.sleep(DELAY)

        with self.assertRaises(TimeoutError):
            raises_timeout_error().await()

        @processes(N, timeout=2*DELAY)
        def no_timeout_error():
            time.sleep(DELAY)

        no_timeout_error().await()


    def test_future_function(self):

        @processes(N)
        def returns_function():
            def f():
                return True
            return f

        true = returns_function().await()
        assert true()


if __name__ == "__main__":
    unittest.main()
