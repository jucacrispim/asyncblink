# -*- coding: utf-8 -*-

import asyncio
import tornado
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.testing import AsyncTestCase, gen_test
from asyncblink import signal


AsyncIOMainLoop().install()


class AsyncBlinkTest(AsyncTestCase):
    def setUp(self):
        super(AsyncBlinkTest, self).setUp()

        self.signal = signal('test-signal')

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    @gen_test
    def test_send(self):
        self.CORO_CALLED = False
        self.RECV_CALLED = False

        @asyncio.coroutine
        def coro_receiver(sender):
            self.CORO_CALLED = True
            return 'coro!'

        def receiver(sender):
            self.RECV_CALLED = True
            return 'recv!'

        self.signal.connect(coro_receiver)
        self.signal.connect(receiver)

        self.signal.send('sender!')

        # shitty sleep.
        yield from asyncio.sleep(.0001)

        self.assertTrue(self.RECV_CALLED)
        self.assertTrue(self.CORO_CALLED)
