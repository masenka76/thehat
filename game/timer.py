import asyncio


class Timer:
    """Asynchronous timer"""

    def __init__(self, timeout, callback, *args, **kwargs):
        self._timeout = timeout
        self._callback = callback
        self._args = args
        self._kwargs = kwargs
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback(*self._args, **self._kwargs)

    def cancel(self):
        self._task.cancel()


class Scheduler(Timer):
    """Asynchronous scheduler"""

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._task = asyncio.ensure_future(self._job())
        await self._callback(*self._args, **self._kwargs)
