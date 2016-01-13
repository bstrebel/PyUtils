#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging, logging.config
from logutils import log_level
from ConfigParser import ConfigParser


class Options(object):

    def __init__(self, options={}, args=None, config=None, config_path=['./', '~/.', '/etc/'], prefix=None):

        self._options = options
        self._args = args
        self._opts = vars(args) if args is not None else {}
        self._prefix = prefix
        self._config = config
        self._config_path = config_path
        self._config_file = None
        self._config_parser = None
        self._logger = None
        self._home = os.path.expanduser('~')
        self._script, ext = os.path.splitext(os.path.basename(sys.argv[0]))
        self._path = os.path.dirname(sys.argv[0])
        self._cwd = os.getcwd()

    def __getitem__(self, key):

        config = self._config_parser
        if config and config.has_section('options') and config.has_option('options', key):
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
        if self._config is not None:
            if self._config_file is None:
                # check args and default from options
                if isinstance(self._config, str):
                    if self._config.startswith('['):
                        key = self._config[1:-1]
                        self._config_file = self.__getitem__(key)
                    else:
                        self.config_file = self._config
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
        if self._config is not None:
            if self._config_parser is None:
                if self.config_file and os.path.isfile(self.config_file):
                    self._config_parser = ConfigParser(self._options)
                    self._config_parser.optionxform = str
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

    def get(self, key, default=None, type=str):

        # required to restore shadowed __builtin__.type()
        import __builtin__

        if default is not None:
            _type = __builtin__.type(default)
        else:
            _type = type

        val = self.__getitem__(key)

        if val is not None:

            try:
                if isinstance(val, str):
                    if _type is str:
                        return val
                    elif _type is int:
                        return int(val)
                    elif _type is float:
                        return float(val)
                    elif _type is bool:
                        if val.lower() in ['true', 'on', 'yes', '1']:
                            return True
                        elif val.lower() in ['false', 'off', 'no', '0']:
                            return False
                        else:
                            # ignore value error
                            pass
                    else:
                        # ignore unsupported target type
                        pass

                elif isinstance(val, int):
                    if _type is int:
                        return val
                    elif _type is float:
                        return float(val)
                    elif _type is str:
                        return str(val)
                    elif _type is bool:
                        if val == 0:
                            return False
                        else:
                            return True
                    else:
                        # ignore unsupported target type
                        pass

                elif isinstance(val, bool):
                    if _type is bool:
                        return val
                    elif _type is str:
                        return str(val)
                    elif _type is int:
                        if val == True:
                            return 1
                        else:
                            return 0
                    elif _type is float:
                        if val == True:
                            return float(1)
                        else:
                            return float(0)
                    else:
                        # ignore unsupported target type
                        pass
                else:
                    # ignore unsupported source type
                    return val
            except:
                # type conversion error
                return default

        # not found error
        return default

    def update(self, options):
        self._options.update(options)