#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time

def strflocal(tm=None, format='%Y-%m-%d %H:%M:%S'):

    if not tm:
        tm = time.time() * 1000

    # try:
    #     # epoch value in seconds
    #     lt = time.localtime(tm)
    # except ValueError:
    #     # epoch value in milliseconds
    #     lt = time.localtime(tm/1000)

    lt = time.localtime(tm/1000)

    return time.strftime(format, lt)
