'''
This module implements a simple size-limited cache/set with O(1) FIFO insertion
and O(1) membership test. Stream sources use this to detect new items by
maintaining a cache of recent URLs.
'''

from collections import deque

class Cache:

    def __init__(self, size=500):
        self.size = size
        self._items = set()
        self._queue = deque()

    def __contains__(self, x):
        return x in self._items

    def add(self, x):
        if x in self._items:
            return
        self._items.add(x)
        self._queue.appendleft(x)
        if len(self._queue) > self.size:
            x = self._queue.pop()
            self._items.remove(x)
