#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from time import *
from datetime import *


def strflocal(tm=None, format='%Y-%m-%d %H:%M:%S'):
    ''' String from local time
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
        tm = time()

    # convert floating point to int/long
    tm = int(tm)

    if len(str(tm)) == 13:
        # concvert milliseconds to seconds
        tm = tm/1000

    lt = localtime(tm)

    return strftime(format, lt)


def localfstr(spec, format=None):
    ''' Local time from string
    :param spec: time specification string
    :param format: format of time string
    :return: unix timestamp (seconds) since 1970, multiply with 1000 for milliseconds
    '''

    if format is not None:
        return int(mktime(datetime.strptime(spec, format).timetuple()))

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    delta = 0

    _year = None

    for token in spec.split():

        if token.lower() in ['now', 'heute', 'jetzt']:
            pass
        elif token.lower() in ['yesterday', 'gestern']:
            day = day - 1
        elif token.lower() in ['at', 'vor', 'um']:
            pass
        elif token[:1] == '+' or token[:1] == '-' or token[-1] in 'smhd':
            if token[-1] in 'smhd':
                unit = token[-1]
                token = token[:-1]
            else:
                unit = 's'
            if token[:1] in '+-':
                op = token[:1]
                token = token[1:]
            else:
                op = '-'
            val = float(token.replace(',', '.'))
            delta = int(val * {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}.get(unit, 's'))
            if op == '-': delta = delta * -1
        elif ':' in token:
            # 13:42[:05]
            tt = token.split(':')
            hour = int(tt[0])
            minute = int(tt[1])
            if len(tt) > 2: second = int(tt[2])
            else: second = 0
        elif '.' in token:
            # 27.9.16
            hour = minute = second = 0
            dt = token.split('.')
            day = int(dt[0])
            month = int(dt[1])
            if len(dt) > 2: _year = dt[2]
        elif '/' in token:
            # 9/27/16
            hour = minute = second = 0
            dt = token.split('/')
            month = int(dt[0])
            day = int(dt[1])
            if len(dt) > 2: _year = dt[2]
        elif '-' in token:
            # 2016-09-27
            hour = minute = second = 0
            dt = token.split('-')
            year = int(dt[0])
            month = int(dt[1])
            day = int(dt[2])
        else:
            # call expression parser
            pass

    if _year is not None:
        if len(_year) == 2: _year = str(year)[:2] + _year
        year = int(_year)

    return int(mktime(datetime(year, month, day, hour, minute, second).timetuple())) + delta
