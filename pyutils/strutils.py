#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def integer(val):
    if isinstance(val, int):
        return val
    else:
        if val.isnumeric():
            return int(val)
    return None

def strsplit(str):
    return re.findall(r"[\w']+", str)

