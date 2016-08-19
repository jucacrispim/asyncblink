# -*- coding: utf-8 -*-

import asyncio
try:
    from asyncio import ensure_future
except ImportError:
    from asyncio import async as ensure_future
from collections import defaultdict
from blinker import Signal
from blinker.base import ANY
from blinker._utilities import hashable_identity


class AsyncSignal(Signal):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # the default scheduler is a dummy one, used to wrap
        # values that are not coroutines
        self._recievers_schedulers = defaultdict(lambda: lambda v:v)

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

        return [(reciever, self._recievers_schedulers[
            hashable_identity(reciever)](value))
                for reciever, value in super().send(*sender, **kwargs)]

    def connect(self, receiver, sender=ANY, weak=True, scheduler=None):
        """Connect *receiver* to signal events sent by *sender*.

        :param receiver: A callable.  Will be invoked by :meth:`send` with
          `sender=` as a single positional argument and any \*\*kwargs that
          were provided to a call to :meth:`send`.

        :param sender: Any object or :obj:`ANY`, defaults to ``ANY``.
          Restricts notifications delivered to *receiver* to only those
          :meth:`send` emissions sent by *sender*.  If ``ANY``, the receiver
          will always be notified.  A *receiver* may be connected to
          multiple *sender* values on the same Signal through multiple calls
          to :meth:`connect`.

        :param weak: If true, the Signal will hold a weakref to *receiver*
          and automatically disconnect when *receiver* goes out of scope or
          is garbage collected.  Defaults to True.

        :param scheduler: Callable used to ensure the execution of a future.
          Note that if you do not provide an ``schedule`` and ``reciever``
          is a function decorated with :func:`asyncio.coroutine`,
          :func:`asyncio.ensure_future` will be used.

        """
        reciever = super().connect(receiver, sender, weak)
        reciever_id = hashable_identity(receiver)
        if scheduler or asyncio.coroutines.iscoroutinefunction(receiver):
            if not scheduler:
                scheduler = ensure_future

            self._recievers_schedulers[reciever_id] = scheduler

        return reciever


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
