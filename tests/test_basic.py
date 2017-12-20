# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:04:39
# Last modified: 2017-12-19 20:42:59

"""
Test for Assist
"""
import configparser

import pytest

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
        assist.comments = 'This is a test comment'
        assist.start()

    def test_getting(self):
        assist = EA.getAssist('Test')
        assert assist.ex_dir == 'tests/Experiments/'

    def test_start_exception(self):
        assist = EA.getAssist('Test')
        s = 'Assist has been locked,  can not add more comments'
        with pytest.raises(Exception) as excinfo:
            assist.comments = 'This is a test.'
        assert str(excinfo.value) == s
