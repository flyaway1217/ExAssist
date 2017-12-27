# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-25 13:59:12
# Last modified: 2017-12-27 10:25:47

"""
Deal with the tempalte.
"""

import os
import json
import configparser
import collections

from mako.template import Template


def gather_experiments(ex_dir):
    names = os.listdir(ex_dir)
    names = [int(s) for s in names if s.isdecimal()]
    names = sorted(names, reverse=True)
    names = [str(s) for s in names]
    reval = []
    for name in names:
        path = os.path.join(ex_dir, name, 'run.json')
        try:
            with open(path, encoding='utf8') as f:
                value = json.load(f)
            record = []
            record.append(name)
            record.append(value.get('start_time', None))
            record.append(value.get('stop_time', None), )
            record.append(value.get('lapse_time', None))
            record.append(value.get('cpu_time', None))
            record.append(value.get('status', None))
            record.append(value.get('comments', None))
            record.append(value.get('result', None))
            reval.append(record)
        except FileNotFoundError:
            continue
    return reval


def generate_index(template_path, ex_dir):
    path = os.path.join(template_path, 'index.html')
    tp = Template(filename=path)
    records = gather_experiments(ex_dir)
    s = tp.render(records=records)

    path = os.path.join(ex_dir, 'index.html')
    with open(path, 'w', encoding='utf8') as f:
        f.write(s)


def generate_ex_index(template_path, ex_path):
    path = os.path.join(template_path, 'ex.html')
    tp = Template(filename=path)

    path = os.path.join(ex_path, 'run.json')
    with open(path, encoding='utf8') as f:
        result = json.load(f)

    path = os.path.join(ex_path, 'config.ini')
    config = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())
    config.read(path, encoding='utf8')

    con = collections.defaultdict(dict)
    for section in config.sections():
        for name, value in config.items(section):
            con[section][name] = value

    s = tp.render(config=con, result=result)

    path = os.path.join(ex_path, 'index.html')
    with open(path, 'w', encoding='utf8') as f:
        f.write(s)
