# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:04:39
# Last modified: 2017-12-18 22:01:55

"""
Test for Assist
"""
import ExAssist as EA
import configparser


class TestEA:
    @classmethod
    def setup_class(cls):
        assist = EA.getAssist('Test')
        assist.ex_dir = 'tests/Experiments/'
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read('tests/config.ini', encoding='utf8')
        assist.config = config
        assist.start()

    def test_getting(self):
        assist = EA.getAssist('Test')
        assert assist.ex_dir == 'tests/Experiments/'
