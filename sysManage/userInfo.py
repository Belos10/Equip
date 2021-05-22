# globalvar.py
# !/usr/bin/python
# -*- coding: utf-8 -*-

def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


# a.py
# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys

_init()  # 初始化全局变量管理模块

set_value('totleUserInfo', None)  # 设置变量值 val_a = 80
