#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time

def strflocal(tm=None, format='%Y-%m-%d %H:%M:%S'):

    if format == None:
        if tm is None:
            return 'None'
        elif tm == 0:
            return '0'
        else:
            format = '%Y-%m-%d %H:%M:%S'

    if tm is None:
        tm = time.time()

    # convert floating point to int/long
    tm = int(tm)

    if len(str(tm)) == 13:
        # concvert milliseconds to seconds
        tm = tm/1000

    lt = time.localtime(tm)

    return time.strftime(format, lt)
