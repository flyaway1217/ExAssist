# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:05:07
# Last modified: 2018-01-26 15:45:03

"""
"""

import threading
import traceback

from ExAssist import assist

__all__ = ['getAssist', 'start']
__version__ = '0.2.0'


_lock = threading.RLock()


def _acquireLock():
    """
    Acquire the module-level lock for serializing access to shared data.

    This should be released with _releaseLock().
    """
    if _lock:
        _lock.acquire()


def _releaseLock():
    """
    Release the module-level lock acquired by calling _acquireLock().
    """
    if _lock:
        _lock.release()


class Manager:
    def __init__(self):
        self.assistDict = {}

    def getAssist(self, name):
        """
        Get a observer with specified name, creating it if
        it doesn't yet exit.

        Args:
            name: str - The name of observer.
        """
        rv = None
        if not isinstance(name, str):
            raise TypeError('A assist name must be a string')
        _acquireLock()
        try:
            if name in self.assistDict:
                rv = self.assistDict[name]
            else:
                rv = assist.Assist(name)
                rv.manager = self
                self.assistDict[name] = rv
        finally:
            _releaseLock()
        return rv


manager = Manager()


class start:
    def __init__(self, assist):
        self._assist = assist

    def __enter__(self):
        self._assist._start()
        return self._assist

    def __exit__(self, exc_type, exc_value, trace):
        if any((exc_type, exc_type, trace)):
            s = traceback.format_exc()
            if exc_type == KeyboardInterrupt:
                self._assist._end('Aborted', s)
                return True
            else:
                self._assist._end('Failed', s)
                print(s)
                return True
        else:
            self._assist._end('Completed')
            return True


def getAssist(name):
    return manager.getAssist(name)
