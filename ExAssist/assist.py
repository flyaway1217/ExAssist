# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-11-23 10:28:17
# Last modified: 2017-12-26 10:13:06

"""
Basic Assist of Experiment.
"""

import os
import json
import collections
import time
import configparser
import shutil
from datetime import timedelta

from ExAssist import host_info
from ExAssist import template


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
        self._config = configparser.ConfigParser()
        self._comments = None
        self._locked = False
        self._path = None

        self._info = collections.defaultdict(dict)
        self._run = dict()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if not self._locked:
            self._config = value

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        if not self._locked:
            print(value)
            self._comments = value

    @property
    def ex_dir(self):
        return self._ex_dir

    @ex_dir.setter
    def ex_dir(self, value):
        # Once started,  ex_dir can not be modified.
        if not self._locked:
            self._ex_dir = value

    @property
    def info(self):
        if self._locked:
            return self._info
        else:
            return collections.defaultdict(dict)

    @property
    def run_path(self):
        # Means nothing before started.
        if self._locked:
            return self._path
        else:
            return None

    ########################################################
    # Private methods
    ########################################################
    def _init_experiment(self):
        """Initialize the experiment.

        This method does following things:

        1. Create the root directory if it does not exist.
            1.a Copy the js and css directory into root directory.
        2. Find the max index of sub directoreis.
        3. Create a new directory.
        4. Return the path
        """
        # Step 1
        dir_name = self._ex_dir
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

            # Copy all the css and js files.
            src = os.path.join(os.path.dirname(__file__), 'templates/css')
            dest = os.path.join(dir_name, 'css')
            shutil.copytree(src, dest)

            src = os.path.join(os.path.dirname(__file__), 'templates/js')
            dest = os.path.join(dir_name, 'js')
            shutil.copytree(src, dest)

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
                os.path.join(self._path, 'info.json'), self._info)

    def _save_run(self):
        self._write_json(
                os.path.join(self._path, 'run.json'), self._run)

    def _start(self):
        if not self._locked:
            self._start_time = time.process_time()
            # Clear the state
            self._run = dict()
            self._info = collections.defaultdict(dict)

            start_time = time.time()
            strtime = time.strftime(
                     '%Y-%m-%d %H:%M:%S', time.localtime(start_time))

            self._path = self._init_experiment()
            self._write_config()
            self._locked = True

            self._run['host_info'] = self._get_host_info()
            self._run['start_time'] = strtime
            self._run['comments'] = self._comments

    def _end(self, status, traceback=None):
        if self._locked:
            self._run['status'] = status
            self._end_time()
            if traceback is not None:
                self._run['traceback'] = traceback
            self._save_run()
            self._save_info()

            # Html related
            template.generate_index(self._ex_dir)
            template.generate_ex_index(self._path)

            self._clear_status()

    def _end_time(self):
        # CPU time
        end_time = time.process_time()
        cpu_lapse = end_time - self._start_time
        strtime = timedelta(seconds=cpu_lapse)
        self._run['cpu_time'] = str(strtime)

        # Stop time
        end_time = time.time()
        strtime = time.strftime(
                 '%Y-%m-%d %H:%M:%S', time.localtime(end_time))
        self._run['stop_time'] = strtime

        # Lapse time
        start_time = time.strptime(self._run['start_time'],
                                   '%Y-%m-%d %H:%M:%S')
        start_time = time.mktime(start_time)
        time_lapse = end_time - start_time
        strtime = timedelta(seconds=time_lapse)
        self._run['lapse_time'] = str(strtime)

    def _clear_status(self):
        # clear all the states
        self._locked = False
        self._path = None
        self._start_time = None
