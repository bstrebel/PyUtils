#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, datetime

def strflocal(tm=None, format='%Y-%m-%d %H:%M:%S'):
    '''
    :param tm: timestamp (seconds or milliseconds)
    :param format: output format
    :return: formatted time string
    '''
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

def timestamp(spec, format='%Y-%m-%d %H:%M:%S'):
    '''
    :param spec: time specification string
    :param format: format of time string
    :return: unix timestamp (seconds) since 1970, multiply with 1000 for milliseconds
    '''
    return int(time.mktime(datetime.datetime.strptime(spec, format).timetuple()))