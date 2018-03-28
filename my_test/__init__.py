#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"
__Date__ = "2018/3/26 下午1:24"

import os
import yaml

base_path = os.path.dirname(os.path.abspath(__file__))
config = dict()
with open(base_path + "/../config/config.yaml") as f:
    config = yaml.load(f)

admin_start = False
