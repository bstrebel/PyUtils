#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging


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
