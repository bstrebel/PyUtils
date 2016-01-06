#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging, logging.config
from logutils import log_level
from ConfigParser import ConfigParser


class Options(object):

    def __init__(self, prefix=None, args=None, options={}, config_path=['./', '~/.', '/etc/']):
        self._options = options
        self._args = args
        self._opts = vars(args)
        self._prefix = prefix
        self._config_path = config_path
        self._home = os.path.expanduser('~')
        self._script, ext = os.path.splitext(os.path.basename(sys.argv[0]))
        self._path = os.path.dirname(sys.argv[0])
        self._cwd = os.getcwd()
        self._config_file = None
        self._config_parser = None
        self._logger = None

    def __getitem__(self, key):

        if self._config_parser:
            default = self._config_parser.get('options', key)
        else:
            default = self._options.get(key, None)

        # check command line options (1)
        if self._opts.get(key):
            return self._opts[key]

        # check environment (2)
        if self._prefix:
            return os.environ.get(self._prefix + '_' + key.upper(), default)

        return default

    def __setitem__(self, key, value):
        self._options[key] = value

    def __getattr__(self, key):
        return self.__getitem__(key)

    @property
    def config_file(self):
        if self._config_file is None:
            # check args and default from options
            self._config_file = self.__getitem__('config')
            if self._config_file:
                self._config_file = os.path.expanduser(self._config_file)
            else:
                # calculate config file name from patch and script name
                for path in self._config_path:
                    path = os.path.expanduser(path)
                    config = os.path.join(path, self._script + '.cfg')
                    if os.path.isfile(config):
                        self._config_file = config
                        break
        return self._config_file

    @property
    def config_parser(self):
        if self._config_parser is None:
            if self.config_file and os.path.isfile(self.config_file):
                self._config_parser = ConfigParser(self._options)
                self._config_parser.read(self.config_file)
        return self._config_parser

    @property
    def logger(self):
        if self._logger is None:
            self._logger = logging.getLogger()
            if self.config_parser:
                if self._config_parser.has_section('loggers'):
                    logging.config.fileConfig(self.config_file)
            self._logger.setLevel(log_level(self.__getitem__('loglevel')))
        return self._logger
