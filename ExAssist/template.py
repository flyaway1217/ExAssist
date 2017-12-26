# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-12-25 13:59:12
# Last modified: 2017-12-26 10:14:37

"""
Deal with the tempalte.
"""

import os
import json

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
            record.append(value['start_time'])
            record.append(value['stop_time'])
            record.append(value['lapse_time'])
            record.append(value['cpu_time'])
            record.append(value['status'])
            record.append(value['comments'])
            reval.append(record)
        except FileNotFoundError:
            continue
    return reval


def generate_index(ex_dir):
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    tp = Template(filename=path)
    records = gather_experiments(ex_dir)
    s = tp.render(records=records)

    path = os.path.join(ex_dir, 'index.html')
    with open(path, 'w', encoding='utf8') as f:
        f.write(s)


def generate_ex_index(ex_path):
    path = os.path.join(os.path.dirname(__file__), 'templates/ex.html')
    tp = Template(filename=path)

    path = os.path.join(ex_path, 'run.json')
    with open(path, encoding='utf8') as f:
        result = json.load(f)

    s = tp.render(result=result)

    path = os.path.join(ex_path, 'index.html')
    with open(path, 'w', encoding='utf8') as f:
        f.write(s)
