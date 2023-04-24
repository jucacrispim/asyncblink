# -*- coding: utf-8 -*-

import asyncio
from collections import defaultdict
import inspect
from blinker import Signal
from blinker.base import ANY
from blinker._utilities import hashable_identity


class AsyncSignal(Signal):
    """AsyncSignal can handle sync and coroutine functions as receivers.
    Note that when using a coroutine as receiver you will get a task
    as the result. You must await it yourself to get the result of the
    coroutine
    """

    _tasks = set()

    def receivers_for(self, sender):
        for receiver in super().receivers_for(sender):
            if asyncio.iscoroutinefunction(receiver):
                def wrap(*args, **kwargs):
                    t = asyncio.ensure_future(receiver(*args, **kwargs))
                    type(self)._tasks.add(t)
                    t.add_done_callback(lambda t: type(self)._tasks.remove(t))
                    return t

                yield wrap

            else:
                yield receiver

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
