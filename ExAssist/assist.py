# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-11-23 10:28:17
# Last modified: 2020-12-23 14:36:49

"""
Basic Assist of Experiment.
"""

import os
import json
import collections
import time
import configparser
from configparser import ConfigParser
import shutil
from argparse import Namespace
from datetime import timedelta
from typing import Union

from ExAssist import host_info
from ExAssist import template


class Assist:
    """
    Attributes:
        - name: The name of observer.
        - _ex_dir: Directory of all experiments.
        - _comments: Comments for current experiment.
        - _started: Indicate if the assist is locked.
        - _path: The directory of current experiment.
    """
    def __init__(self, name: str):
        self.name = name

        self._ex_dir = 'Experiments/'
        self._config = None

        # If this instance is locked, its
        # meta data can not be modified,  such
        # as config_path, ex_dir
        self._locked = False
        self._path = None
        self._comments = None
        self._tempate_path = './templates'

        self._current_info = collections.defaultdict(dict)
        self._result = collections.defaultdict(dict)
        self._info = []
        self._run = dict()

    ########################################################
    # Public methods
    ########################################################
    def step(self):
        """ Move to next epoch.
        """
        if self._locked:
            self._info.append(self._current_info)
            self._current_info = collections.defaultdict(dict)

    def set_config(self, config: Union[dict, ConfigParser, Namespace]):
        """Set the config settings.
           This method can only be called before entering context environment.

        This method can take one of the followings as input:
            - A dictionary object that contains all the
              configurations as (key, value)
            - A argparse.namespace object.
              This namespace object should contains all the configurations.
            - A ConfigParser object that loads configurations
              from config files.

        Thid method provides two functions:
            1. No matter what the input argument is, this method will
               transform all the configurations into a namespace object.
            2. If a key starts with 'run_' and self is in the dev mode,
               this method will automatically update the value of that
               key with current running experiment directory.
        """
        if self._locked:
            return
        else:
            config = self._to_dict(config)
            self._config = Namespace()
            for key, value in config.items():
                setattr(self._config, key, value)

    ########################################################
    # Properties
    ########################################################
    @property
    def template(self):
        """The path of template file.
        """
        return self._tempate_path

    @template.setter
    def template(self, value):
        if not self._locked:
            self._tempate_path = value

    @property
    def ex_dir(self):
        """The root directory of all experiments.
        """
        return self._ex_dir

    @ex_dir.setter
    def ex_dir(self, value):
        # Once started,  ex_dir can not be modified.
        if not self._locked:
            self._ex_dir = value

    @property
    def info(self):
        if self._locked:
            return self._current_info
        # it is meaningless to use info when it is unlocked.
        else:
            return collections.defaultdict(dict)

    @property
    def result(self):
        if self._locked:
            return self._result
        else:
            return collections.defaultdict(dict)

    @property
    def run_path(self):
        # Means nothing before started.
        if self._locked:
            return self._path
        else:
            return None

    @property
    def epoch(self):
        """Returnt the current epoch.
        """
        return len(self._info)

    @property
    def config(self):
        """Return the config object.
        """
        if self._locked:
            return self._config
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
        src = os.path.join(self._tempate_path, 'css')
        dest = os.path.join(dir_name, 'css')
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)

        src = os.path.join(self._tempate_path, 'js')
        dest = os.path.join(dir_name, 'js')
        if os.path.exists(dest):
            shutil.rmtree(dest)
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
        self._run['result'] = self._result
        self._write_json(
                os.path.join(self._path, 'run.json'), self._run)

    def _save_config(self):
        self._write_json(
                os.path.join(self._path, 'config.json'), vars(self._config))

    def _start(self):
        if not self._locked:
            self._start_time = time.process_time()
            # Clear the state
            self._run = dict()
            self._current_info = collections.defaultdict(dict)
            self._info = []

            start_time = time.time()
            strtime = time.strftime(
                     '%Y-%m-%d %H:%M:%S', time.localtime(start_time))

            self._path = self._init_experiment()
            self._set_runtime_config()
            self._save_config()
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
            template.generate_index(self._tempate_path, self._ex_dir)
            template.generate_ex_index(self._tempate_path, self._path)

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
        """Clear all the states
        """
        self._locked = False
        self._path = None
        self._start_time = None

        self._current_info = collections.defaultdict(dict)
        self._info = []
        self._result = collections.defaultdict(dict)

    def _read_config(self):
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read(self._config_path, encoding='utf8')
        self._config = config

    def _to_dict(self, config: Union[dict, ConfigParser, Namespace]):
        if type(config) == dict:
            return config
        elif type(config) == ConfigParser:
            reval = dict()
            sections = config.sections()
            for sec in sections:
                for key, value in config.items(sec):
                    if sec == 'run':
                        key = '_'.join([sec, key])
                    reval[key] = value
            return reval
        elif type(config) == Namespace:
            return vars(config)
        else:
            raise Exception('Unrecognized config object!')

    def _set_runtime_config(self):
        names = list(self._config.__dict__.keys())
        for name in names:
            if name.startswith('run_'):
                if name == 'run_comments':
                    self._comments = getattr(self._config, name)
                else:
                    # Delete the run_* attribute
                    value = getattr(self._config, name)
                    delattr(self._config, name)

                    value = os.path.join(self._path, value)
                    name = name[4:]
                    setattr(self._config, name, value)
