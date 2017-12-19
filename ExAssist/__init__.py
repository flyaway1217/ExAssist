# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-18 21:05:07
# Last modified: 2017-12-18 21:07:50

"""
"""

from ExAssist import assist

__all__ = ['getAssist']


manager = assist.Manager()


def getAssist(name):
    return manager.getAssist(name)
