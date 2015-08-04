import time
from functools import wraps
import asyncio


class RateLimited:
    def __init__ (self, max_per_second):
        self.lock = asyncio.Lock()
        self.calls = 0
        self.last_call = 0
        self.max_calls = max_per_second

    def wait(self):
        if self.calls >= self.max_calls:
            while int(time.time()) == self.last_call:
                yield from asyncio.sleep(0.01)

        if int(time.time()) != self.last_call:
            self.calls = 0

        self.last_call = int(time.time())
        self.calls += 1
        return

    def __call__(self, func):
        @asyncio.coroutine
        def rate_limited_function(*args, **kwargs):
            with (yield from self.lock):
                yield from self.wait()
                return (yield from func(*args, **kwargs))

        return rate_limited_function
