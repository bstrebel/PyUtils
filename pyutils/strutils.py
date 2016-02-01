#!/usr/bin/env python
# -*- coding: utf-8 -*-

def integer(val):
    if isinstance(val, int):
        return val
    else:
        if val.isnumeric():
            return int(val)
    return None
