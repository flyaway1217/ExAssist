# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:04:39
# Last modified: 2017-12-25 16:13:04

"""
Test for Assist
"""
import collections
import configparser

import ExAssist as EA


class TestEA:
    @classmethod
    def setup_class(cls):
        assist = EA.getAssist('Test')
        assist.ex_dir = 'tests/Experiments/'
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read('tests/config.ini', encoding='utf8')
        assist.config = config
        # assist.comments = 'This is a test comment'

    def test_config(self):
        """Test for config.

        1. Can not modify the config once started.
        2. Always can acess the config.
        """
        assist = EA.getAssist('Test')
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read('tests/config.ini', encoding='utf8')

        config_tmp = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        assert assist.config == config

        with EA.start(assist) as assist:
            assert assist.config == config
            assist.config = config_tmp
            assert assist.config == config

        assist.config = config_tmp
        assert assist.config == config_tmp

    def test_comments(self):
        """ Test for Comments.

        1. Can not modify the comments once started.
        2. Always can acess the comments.
        """
        assist = EA.getAssist('Test')
        comments = 'First comment'

        assert assist.comments is None

        assist.comments = comments
        assert assist.comments == comments
        assert assist._locked is False

        with EA.start(assist) as assist:
            assert assist._locked is True
            assist.comments = 'Second comment'
            assert assist.comments == comments

        assert assist._locked is False
        assist.comments = 'Second comment'
        assert assist.comments == 'Second comment'

    def test_ex_dir(self):
        """ Test for ex_dir.

        1. Can not modify the ex_dir once started.
        2. Always can acess the ex_dir.
        """
        assist = EA.getAssist('Test')
        assert assist.ex_dir == 'tests/Experiments/'

        ex_dir = 'test/Ex2'
        assist.ex_dir = ex_dir
        assert assist.ex_dir == ex_dir

        assist.ex_dir = 'tests/Experiments/'
        with EA.start(assist) as assist:
            assist.ex_dir = ex_dir
            assert assist.ex_dir == 'tests/Experiments/'

        assist.ex_dir = ex_dir
        assert assist.ex_dir == ex_dir

        assist.ex_dir = 'tests/Experiments/'

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

    def test_run_path(self):
        """ Test for run_path.

        Only accessable after started.
        """
        assist = EA.getAssist('Test')
        assert assist.run_path is None

        with EA.start(assist) as assist:
            assert type(assist.run_path) == str
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
