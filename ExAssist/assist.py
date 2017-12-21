# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-11-23 10:28:17
# Last modified: 2017-12-20 20:21:59

"""
Basic Assist of Experiment.
"""

import os
import json
import atexit
import collections

from ExAssist import host_info


class Assist:
    """
    Attributes:
        - name: The name of observer.
        - _ex_dir: Directory of all experiments.
        - _config: Config object of current Assist.
        - _comments: Comments for current experiment.
        - _started: Indicate if the assist is locked.
        - _path: The directory of current experiment.
    """
    def __init__(self, name):
        self.name = name
        self._ex_dir = 'Experiments/'
        self._config = None
        self._comments = None
        self._started = False
        self._path = None
        atexit.register(self._save_info)

        self.info = collections.defaultdict(dict)

    def start(self):
        if not self._isLocked():
            self._path = self._init_experiment()
            self._write_config()
            self._started = True

            info = self._get_host_info()
            self._write_json(
                    os.path.join(self._path, 'host.json'), info)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if self._isLocked():
            raise Exception(
                    'Assist has been locked,  can not add more configs')
        else:
            self._config = value

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        if self._isLocked():
            raise Exception(
                    'Assist has been locked,  can not add more comments')
        else:
            self._comments = value

    @property
    def ex_dir(self):
        return self._ex_dir

    @ex_dir.setter
    def ex_dir(self, value):
        if self._isLocked():
            raise Exception(
                'Assist has been locked,  can not set experiments directory.')
        else:
            self._ex_dir = value

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
        dir_name = self._ex_dir
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
