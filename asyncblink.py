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
        # Using '*sender' rather than 'sender=None' allows 'sender' to be
        # used as a keyword argument- i.e. it's an invisible name in the
        # function signature.
        if len(sender) == 0:
            sender = None
        elif len(sender) > 1:
            raise TypeError('send() accepts only one positional argument, '
                            '%s given' % len(sender))
        else:
            sender = sender[0]

        # the only difference is here. If it's a coroutine,
        # run it with asyncio.async()
        receivers = self.receivers_for(sender) or []
        return_list = []

        for receiver in receivers:
            ret = receiver(sender, **kwargs)
            if asyncio.coroutines.iscoroutine(ret):
                ret = ensure_future(ret)
            return_list.append((receiver, ret))

        return return_list


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
