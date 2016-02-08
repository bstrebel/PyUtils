#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging

class LogAdapter(logging.LoggerAdapter):
    """
    custom LoggerAdapter implementation to inject extras into log message
    """
    def __init__(self, logger, extra):
        logging.LoggerAdapter.__init__(self, logger, extra)

    def process(self, msg, kwargs):
        if self.extra.get('callback'):
            msg = self.extra['callback'](msg)
        return '[%s] %s' % (self.extra['package'], msg), kwargs

class LogFileHandler(logging.FileHandler):
    """
    advanced FileHandler class with expanduser support
    usage in file based logging configuration:
        [handler_fileHandler]
        formatter=fileFormatter
        level=INFO
        class=pyutils.LogFileHandler
        args=('~/oxsync/oxsync.log', 'a')
    """
    def __init__(self, path, mode='a', endcoding='utf-8'):
        import logging
        path = os.path.expanduser(path)
        logging.FileHandler.__init__(self, path, mode, endcoding)


def get_logger(name=None, level=None):
    """
    default console logger
    :param name: optional name of logger instance
    :param level: initial log level
    :return: the logger object
    """

    # stream handler configuration
    sh = logging.StreamHandler()
    sf = logging.Formatter('%(levelname)-8s %(module)s %(message)s')
    sh.setFormatter(sf)

    root = logging.getLogger(name)
    if level is not None:
        root.setLevel(log_level(level))
    root.addHandler(sh)

    return root

def log_level(level=logging.DEBUG):
    """
    convert string expression to numeric log level
    :param level: log level expression e.g. 'DEBUG'
    :return: numeric log level for logging.setLevel()
    """
    if level is None:
        return logging.DEBUG

    if isinstance(level, str):
        new_level = getattr(logging, level.upper(), None)
        if new_level:
            return new_level
    return level
