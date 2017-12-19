# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-11-23 10:28:17
# Last modified: 2017-12-18 21:46:43

"""
Basic Assist of Experiment.
"""


import threading
import os
import json
import atexit
import collections

from ExAssist import host_info


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


class Assist:
    """

    Attributes:
        - name: The name of observer.
        - ex_dir: Directory of all experiments.
        - _config: Config object of current Assist.
        - _comments: Comments for current experiment.
        - _started: Indicate if the assist is locked.
        - _path: The directory of current experiment.
    """
    def __init__(self, name):
        self.name = name
        self.ex_dir = 'Experiments/'
        self._config = None
        self._comments = None
        self._started = False
        self._path = None
        atexit.register(self._save_info)

        self.info = collections.defaultdict(dict)

    def setConfig(self, config):
        """
        Setup the configuration for current experiments.

        Args:
            config: ConfigParser
        """
        if self._isLocked():
            raise Exception(
                    'Assist has been locked,  can not add more configs')
        else:
            self._config = config

    def setComments(self, comments):
        if self._isLocked():
            raise Exception(
                    'Assist has been locked,  can not add more comments')
        else:
            self._comments = comments

    def start(self):
        if not self._isLocked():
            self._path = self._init_experiment()
            self._write_config()
            self._started = True

            info = self._get_host_info()
            self._write_json(
                    os.path.join(self._path, 'host.json'), info)

    ########################################################
    # Private methods
    ########################################################
    def _init_experiment(self):
        """Initialize the experiment.

        This method does following things:

        1. Create the root directory if it does not exist.
        2. Find the max index of sub directoreis.
        3. Create a new directory.
        4. Return the path
        """
        # Step 1
        dir_name = self.ex_dir
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
        return path

    def _isLocked(self):
        return self._started is True

    def _write_config(self):
        """Write down the config file.
        """
        path = self._path
        path = os.path.join(path, 'config.ini')
        with open(path, 'w', encoding='utf8') as f:
            self._config.write(f)

    def _get_host_info(self):
        return host_info.get_host_info()

    def _write_json(self, path, obj):
        with open(path, 'w', encoding='utf8') as f:
            json.dump(obj, f, indent=0)

    def _save_info(self):
        self._write_json(
                os.path.join(self._path, 'info.json'), self.info)


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
                rv = Assist(name)
                rv.manager = self
                self.assistDict[name] = rv
        finally:
            _releaseLock()
        return rv
