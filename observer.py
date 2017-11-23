# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-11-23 10:28:17
# Last modified: 2017-11-23 13:59:38

"""
Basic Observer of Experiment.
"""


import threading
import os

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


class Observer:
    def __init__(self, name, dir_name='Experiments/'):
        self.name = name
        self._dir_name = dir_name
        self._config = None
        self._comments = None
        self._started = False

    def setConfig(self, config):
        """
        Setup the configuration for current experiments.

        Args:
            config: ConfigParser
        """
        self._config = config

    def setComments(self, comments):
        self._comments = comments

    def start(self):
        if self._started is False:
            self._init_experiment()
            self._started = True

    def loss(self, iteration, loss):
        pass

    def _init_experiment(self):
        """Initialize the experiment.

        This method does following things:

        1. Create the root directory if it does not exist.
        2. Find the max index of sub directoreis.
        3. Create a new directory.
        4. Write down all the configurations.
        """
        # Step 1
        dir_name = self._dir_name
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        # Step 2
        names = os.listdir(dir_name)
        names = [int(s) for s in names if s.isdecimal()]
        if len(names) != 0:
            index = max(names) + 1
        else:
            index = 0

        # Step 3
        path = os.path.join(dir_name, str(index))
        os.mkdir(path)

        # Step 4
        path = os.path.join(path, 'config.ini')
        with open(path, 'w', encoding='utf8') as f:
            self._config.write(f)


class Manager:
    def __init__(self):
        self.observerDict = {}

    def getObserver(self, name):
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
            if name in self.observerDict:
                rv = self.observerDict[name]
            else:
                rv = Observer(name)
                rv.manager = self
                self.observerDict[name] = rv
        finally:
            _releaseLock()
        return rv

#############################################################
# Module functions
#############################################################


manager = Manager()


def getObserver(name):
    return manager.getObserver(name)
