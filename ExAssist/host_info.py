# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Yichu Zhou - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.6.0
#
# Date: 2017-11-24 10:59:35
# Last modified: 2020-12-21 15:57:34

"""
Collect information about the host of an experiment.

TODO:
    1. Python dependency
"""

import os
import platform
import re
import subprocess
import xml.etree.ElementTree as ET
import pkg_resources


__all__ = ['get_host_info']


class IgnoreHostInfo(Exception):
    """Used by host_info_getters to signal that this cannot be gathered."""
    pass


# #################### Default Host Information ###############################
def _hostname():
    return platform.node()


def _os():
    return [platform.system(), platform.platform()]


def _python_version():
    return platform.python_version()


def _cpu():
    if platform.system() == "Windows":
        return platform.processor().strip()
    elif platform.system() == "Darwin":
        os.environ['PATH'] += ':/usr/sbin'
        command = ["sysctl", "-n", "machdep.cpu.brand_string"]
        return subprocess.check_output(command).decode().strip()
    elif platform.system() == "Linux":
        command = ["cat", "/proc/cpuinfo"]
        all_info = subprocess.check_output(command).decode()
        model_pattern = re.compile("^\s*model name\s*:")
        for line in all_info.split("\n"):
            if model_pattern.match(line):
                return model_pattern.sub("", line, 1).strip()


def _gpus():
    try:
        xml = subprocess.check_output(['nvidia-smi', '-q', '-x']).decode()
    except (FileNotFoundError, OSError, subprocess.CalledProcessError):
        raise IgnoreHostInfo()

    gpu_info = {'gpus': []}
    for child in ET.fromstring(xml):
        if child.tag == 'driver_version':
            gpu_info['driver_version'] = child.text
        if child.tag != 'gpu':
            continue
        gpu = {
            'model': child.find('product_name').text,
            'total_memory': int(child.find('fb_memory_usage').find('total')
                                .text.split()[0]),
            'persistence_mode': (child.find('persistence_mode').text ==
                                 'Enabled')
        }
        gpu_info['gpus'].append(gpu)

    return gpu_info


def _packages():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                     for i in installed_packages])
    return installed_packages_list


def get_host_info():
    """Collect some information about the machine this experiment runs on.

    Returns
    -------
    dict
        A dictionary with information about the CPU, the OS and the
        Python version of this machine.

    """
    host_info = {}
    host_info_gatherers = {
            'hostname': _hostname,
            'os': _os,
            'python_version': _python_version,
            'cpu': _cpu,
            'gpu': _gpus,
            'packages': _packages}
    for k, v in host_info_gatherers.items():
        try:
            host_info[k] = v()
        except IgnoreHostInfo:
            pass
    return host_info
