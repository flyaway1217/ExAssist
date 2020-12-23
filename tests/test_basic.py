# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:04:39
# Last modified: 2020-12-23 15:16:36

"""
Test for Assist
"""
import collections
import configparser

import ExAssist as EA
from argparse import Namespace


class TestEA:
    @classmethod
    def setup_class(cls):
        assist = EA.getAssist('Test')
        assist.activate()
        assist.ex_dir = 'tests/Experiments/'
        # config = configparser.ConfigParser(
        #         interpolation=configparser.ExtendedInterpolation())
        # config.read('tests/config.ini', encoding='utf8')
        # assist.
        # assist.comments = 'This is a test comment'
        # assist.config_path = 'tests/config.ini'

    def test_config(self):
        """Test for config.

        1. Load the config file.
        2. Transform the config into dictionary.
        """
        assist = EA.getAssist('Test')
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read('tests/config.ini', encoding='utf8')

        assist.set_config(config)
        with EA.start(assist) as assist:
            assert type(assist.config) == Namespace
            assert assist.config.c1 == '0.0001'
            assert 'run_comments' not in assist.config

    def test_ex_dir(self):
        """ Test for ex_dir.

        1. Can not modify the ex_dir once started.
        2. Always can acess the ex_dir.
        """
        ex_dir1 = 'tests/Experiments/'
        ex_dir2 = 'test/Ex2'
        assist = EA.getAssist('Test')
        assert assist.ex_dir == ex_dir1

        assist.ex_dir = ex_dir2
        assert assist.ex_dir == ex_dir2

        assist.ex_dir = ex_dir1
        with EA.start(assist) as assist:
            assist.ex_dir = ex_dir1
            assert assist.ex_dir == ex_dir1
            assist.ex_dir = ex_dir2
            assert assist.ex_dir == ex_dir1
            assert assist.ex_dir != ex_dir2

        assist.ex_dir = ex_dir2
        assert assist.ex_dir == ex_dir2

        assist.ex_dir = ex_dir1

    def test_info(self):
        """Test for info.

        Only accessable after started.
        """
        assist = EA.getAssist('Test')
        for i in range(100):
            assist.info['loss'][i] = 100-i

        assert assist.info == collections.defaultdict(dict)
        with EA.start(assist) as assist:
            assert assist.info == collections.defaultdict(dict)
            for i in range(100):
                assist.info['loss'][i] = 100 - i
            for i in range(100):
                assert assist.info['loss'][i] == 100 - i

        assert assist.info == collections.defaultdict(dict)

    def test_step(self):
        """Test for steps.

        Only accessable after started.
        """
        assist = EA.getAssist('Test')
        for i in range(100):
            assist.info['loss'][i] = 100-i

        assert assist.info == collections.defaultdict(dict)
        assist.step()
        assist.step()
        assist.step()
        assist.step()
        assert assist.epoch is None
        with EA.start(assist) as assist:
            assert assist.info == collections.defaultdict(dict)
            for i in range(100):
                assist.info['loss'] = 100 - i
                assist.step()
            for i in range(100):
                assert assist._info[i]['loss'] == 100 - i
            assert assist.epoch == 100

        assert assist.epoch is None

    def test_run_path(self):
        """ Test for run_path.

        Only accessable after started.
        """
        assist = EA.getAssist('Test')
        assert assist.run_path is None

        with EA.start(assist) as assist:
            assert type(assist.run_path) == str
            assert assist.config['run']['scores_path'] != '/scores.txt'
        assert assist.run_path is None

    def test_interrupt(self):
        assist = EA.getAssist('Test')
        with EA.start(assist) as assist:
            raise KeyboardInterrupt
        assert assist._run['status'] == 'Aborted'

        with EA.start(assist) as assist:
            raise MemoryError
        assert assist._run['status'] == 'Failed'

    def test_time(self):
        assist = EA.getAssist('Test')
        with EA.start(assist) as assist:
            A = 10000000
            for i in range(A):
                A = A-1
        assert A == 0

    def test_result(self):
        assist = EA.getAssist('Test')
        assert assist.result == collections.defaultdict(dict)
        assist.result['recall'] = 0.9
        assert assist.result == collections.defaultdict(dict)
        with EA.start(assist) as assist:
            assist.result['precision'] = 1.0
            assist.result['recall'] = 0.9
            assert assist.result['precision'] == 1.0
            assert assist.result['recall'] == 0.9
        assert assist.result == collections.defaultdict(dict)

    def test_comments(self):
        assist = EA.getAssist('Test')
        assert assist._comments == 'First comment'

    def test_activate(self):
        assist = EA.getAssist('Test')
        assist.deactivate()
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read('tests/config.ini', encoding='utf8')

        assist.set_config(config)
        with EA.start(assist) as assist:
            assert type(assist.config) == Namespace
            assert assist.config.c1 == '0.0001'
            assert 'run_comments' in assist.config

            assist.template('others/templates/')
            assert assist.template == './templates'
            assist.ex_dir == 'others/experiments/'
            assert assist.ex_dir == 'tests/Experiments/'

            assist.info['var'] = 'var'
            assert len(assist.info) == 0
            assist.result['var'] = 'var'
            assert len(assist.result) == 0

            assert assist.run_path is None
            assert assist.epoch is None
