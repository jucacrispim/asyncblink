# -*- coding: utf-8 -*-

import asyncio
from tornado.testing import AsyncTestCase, gen_test
from asyncblink import signal


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper



class AsyncBlinkTest(AsyncTestCase):
    def setUp(self):
        super(AsyncBlinkTest, self).setUp()

        self.signal = signal('test-signal')

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
            self.CORO_CALLED = True
            return 'coro!'

        self.signal.connect(coro_receiver)
        self.signal.send('sender!')
        # shitty sleep.
        yield from asyncio.sleep(.0001)
        self.assertTrue(self.CORO_CALLED)
