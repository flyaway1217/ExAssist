# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:04:39
# Last modified: 2017-12-21 21:37:27

"""
Test for Assist
"""
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

    def test_getting(self):
        assist = EA.getAssist('Test')
        assert assist.ex_dir == 'tests/Experiments/'

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

    def test_info(self):
        assist = EA.getAssist('Test')
        with EA.start(assist) as assist:
            for i in range(100):
                assist.info['loss'][i] = 100-i
