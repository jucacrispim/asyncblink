# -*- coding: utf-8 -*-

import asyncio
try:
    from asyncio import ensure_future
except ImportError:
    from asyncio import async as ensure_future

from blinker import Signal


class AsyncSignal(Signal):

    # Exact the same as blinker, but using asyncio
    def send(self, *sender, **kwargs):
        """ Emit this signal on behalf of *sender*, passing on \*\*kwargs.

        Returns a list of 2-tuples, pairing receivers with their return
        value. If receiver is a coroutine the return value is a Future.
        The ordering of receiver notification is undefined.

        :param \*sender: Any object or ``None``.  If omitted, synonymous
          with ``None``.  Only accepts one positional argument.

        :param \*\*kwargs: Data to be sent to receivers.

        """

        # tks jek
        def _wrap(value):
            if asyncio.coroutines.iscoroutine(value):
                yield from value
            return value
        return [(receiver, ensure_future(_wrap(value)))
                for receiver, value in super().send(*sender, **kwargs)]


class NamedAsyncSignal(AsyncSignal):
    """A named generic notification emitter."""

    def __init__(self, name, doc=None):
        super(NamedAsyncSignal, self).__init__(doc)

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
