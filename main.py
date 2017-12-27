# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-26 18:55:52
# Last modified: 2017-12-26 18:57:46

"""

"""

import ExAssist as EA
import configparser

assist = EA.getAssist('Test')
assist.ex_dir = 'tests/Experiments/'
config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
config.read('tests/config.ini', encoding='utf8')
assist.config = config

with EA.start(assist) as assist:
    for i in range(100):
        assist.info['loss'] = 100 - i
        assist.step()
    for i in range(100):
        assert assist._info[i]['loss'] == 100 - i
    print(assist._info)
