#!/usr/bin/env python
# -*- coding: utf-8 -*-

def utf8(ref):

    if isinstance(ref, dict):

        for k,v in ref.iteritems():
            if isinstance(v, str):
                ref[k] = v.decode('utf-8', errors='ignore')
        return ref

    elif isinstance(ref, list):

        new = []
        for v in ref:
            if isinstance(v, str):
                new.append(v.decode('utf-8', errors='ignore'))
            else:
                new.append(v)
        return new

    else:

        if isinstance(ref, str):
            return ref.decode('utf-8', errors='ignore')

    return ref


def string(ref):
    if isinstance(ref, unicode):
        return ref.encode('utf-8', errors='ignore')
    return ref



