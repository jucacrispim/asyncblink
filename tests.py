# -*- coding: utf-8 -*-

import asyncio
import sys
from unittest import TestCase
try:
    from tornado import gen, ioloop
    from tornado.platform.asyncio import to_tornado_future
    from tornado.testing import AsyncTestCase, gen_test
    has_tornado = True
except ImportError:
    has_tornado = False

from asyncblink import signal


PY35 = sys.version_info[:2] >= (3, 5)

if has_tornado:
    test_case_class = AsyncTestCase
else:
    msg = 'Tornado not prenset. Not running tests for different schedulers!'
    print('\n{}\n'.format(msg))
    test_case_class = TestCase

def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper



class AsyncBlinkTest(test_case_class):
    def setUp(self):
        super(AsyncBlinkTest, self).setUp()

        self.signal = signal('test-signal')

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def test_send(self):
        self.RECV_CALLED = False

        def receiver(sender):
            self.RECV_CALLED = True
            return 'recv!'

        self.signal.connect(receiver)
        self.signal.send('sender!')
        self.assertTrue(self.RECV_CALLED)

    @async_test
    def test_send_with_coro(self):
        self.CORO_CALLED = False

        @asyncio.coroutine
        def coro_receiver(sender):
            yield from asyncio.coroutine(lambda: None)()
            self.CORO_CALLED = True
            return 'coro!'

        self.signal.connect(coro_receiver)
        r = self.signal.send('sender!')
        yield from r[0][1]
        self.assertTrue(self.CORO_CALLED)

    if PY35:
        @async_test
        async def test_send_async(self):
            self.CORO_CALLED = False
            async def receiver(sender):
                await asyncio.coroutine(lambda: None)()
                self.CORO_CALLED = True

            self.signal.connect(receiver)
            r = self.signal.send('sender')
            await r[0][1]
            self.assertTrue(self.CORO_CALLED)

    if has_tornado:
        @gen_test
        def test_send_with_tornado_coro(self):

            self.TORNADO_CORO_CALLED = False

            @gen.coroutine
            def coro_receiver(sender):
                yield gen.coroutine(lambda: None)()
                self.TORNADO_CORO_CALLED = True
                return 'tornado coro!'

            def scheduler(future):
                loop = ioloop.IOLoop.instance()
                loop.add_future(future, lambda f: f)
                return future

            self.signal.scheduler = scheduler
            self.signal.connect(coro_receiver)

            r = self.signal.send('sender!')
            yield r[0][1]
            self.assertTrue(self.TORNADO_CORO_CALLED)
