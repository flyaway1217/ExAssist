# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:05:07
# Last modified: 2017-12-18 21:50:47

"""
"""

import threading

from ExAssist import assist

__all__ = ['getAssist']


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
            raise TypeError('A observer name must be a string')
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


def getAssist(name):
    return manager.getAssist(name)
