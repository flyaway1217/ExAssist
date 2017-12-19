# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:04:39
# Last modified: 2017-12-18 21:09:17

"""
Test for Assist
"""
import ExAssist as EA
import configparser


def test_host():
    assist = EA.getAssist('Test')
    config = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())
    config.read('tests/config.ini', encoding='utf8')

    assist.setConfig(config)

    assist.start()
    assert 1 == 1
