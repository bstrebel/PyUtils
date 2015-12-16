#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging

class LogAdapter(logging.LoggerAdapter):

    def __init__(self, logger, extra):
        logging.LoggerAdapter.__init__(self, logger, extra)

    def process(self, msg, kwargs):
        if self.extra.get('callback'):
            msg = self.extra['callback'](msg)
        return '[%s] %s' % (self.extra['package'], msg), kwargs

class LogFileHandler(logging.FileHandler):

    def __init__(self, path, mode='a', endcoding='utf-8'):
        import logging
        path = os.path.expanduser(path)
        logging.FileHandler.__init__(self, path, mode, endcoding)


def ConsoleLogger(name=None):

    # stream handler configuration
    sh = logging.StreamHandler()
    sf = logging.Formatter('%(levelname)-7s %(module)s %(message)s')
    sh.setFormatter(sf)

    # logging via LoggerAdapter
    root = logging.getLogger(name)
    root.setLevel(logging.DEBUG)
    root.addHandler(sh)

    return root
