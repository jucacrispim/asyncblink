# -*- coding: utf-8 -*-

import asyncio
import sys
from unittest import IsolatedAsyncioTestCase
from asyncblink import signal


class AsyncBlinkTest(IsolatedAsyncioTestCase):
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

    async def test_send_async(self):
        self.CORO_CALLED = False
        async def receiver(sender):
            async def fn():
                return None
            await fn()
            self.CORO_CALLED = True

        self.signal.connect(receiver)
        r = self.signal.send('sender')
        await r[0][1]
        self.assertTrue(self.CORO_CALLED)
