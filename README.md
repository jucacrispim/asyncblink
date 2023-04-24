AsyncBlink is a small extention to Blinker and enables you to use
coroutines as receivers for your signals.

Install
=======

Installation is simple, via pip:

```sh
   $ pip install asyncblink
```


Usage
=====

Usage is simple, too. Create a signal, connect some receivers to it
and then use the ``send()`` method to trigger all receivers

```python
from asyncblink import signal
my_signal = signal('nice-signal')


async def coro_receiver(sender, **kwargs):
    # an expensive io operation here
    return 'done'

def receiver(sender):
    return 'ok'

my_signal.connect(coro_receiver)
my_signal.connect(receiver)
my_signal.send('some-sender')
```

Other than that, AsyncBlink's usage is the same as Blinker, Take a look at the
`[Blinker documentation](http://pythonhosted.org/blinker/) for further
information.


Why this still exists?
======================

Blinker now supports coroutines via ``signal.async_send``, so why asyncblink
is still alive?

The blinker's implementation awaits for coroutines and it is not what I want
so asyncblink schedules the coroutine and returns a task.


Source Code
===========

Source code is hosted on [github](https://github.com/jucacrispim/asyncblink).
