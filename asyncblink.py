# -*- coding: utf-8 -*-

import asyncio

try:
    ensure_future = asyncio.ensure_future
except ImportError:
    ensure_future = getattr(asyncio, "async")

from collections import defaultdict
import inspect
from blinker import Signal
from blinker.base import ANY
from blinker._utilities import hashable_identity


class AsyncSignal(Signal):

    def __init__(self, *args, **kwargs):
        """ Constructor for AsyncSignal

        :param \*args: Arguments list passed to super() constructor.
        :param \*\*kwargs: Keywork arguments passed to super() constructor.

        .. note::

           Here you can use scheduler=<some-scheduler>. The scheduler is a
           callable used to ensure the execution of a future.
           Note that if you do not provide an ``scheduler`` and the receiver
           function is a coroutine  :func:`asyncio.ensure_future` will be used.

        """
        self.scheduler = kwargs.pop('scheduler', ensure_future)
        super().__init__(*args, **kwargs)

    def send(self, *sender, **kwargs):
        """ Emit this signal on behalf of *sender*, passing on \*\*kwargs.

        Returns a list of 2-tuples, pairing receivers with their return
        value. If receiver is a coroutine the return value is a Future.
        The ordering of receiver notification is undefined.

        :param \*sender: Any object or ``None``.  If omitted, synonymous
          with ``None``.  Only accepts one positional argument.

        :param \*\*kwargs: Data to be sent to receivers.

        """

        ret = []
        for receiver, value in super().send(*sender, **kwargs):
            if self._is_future(value):
                value = self.scheduler(value)

            ret.append((receiver, value))

        return ret

    def _is_future(self, val):
        return inspect.isawaitable(val)


class NamedAsyncSignal(AsyncSignal):
    """A named generic notification emitter."""

    def __init__(self, name, doc=None):
        super().__init__(doc)

        #: The name of this signal.
        self.name = name

    def __repr__(self):
        base = super(NamedAsyncSignal, self).__repr__()
        return "%s; %r>" % (base[:-1], self.name)


class Namespace(dict):
    """A mapping of signal names to signals."""

    def signal(self, name, doc=None):
        """Return the :class:`NamedSignal` *name*, creating it if required.

        Repeated calls to this function will return the same signal object.

        """
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedAsyncSignal(name, doc))


signal = Namespace().signal
