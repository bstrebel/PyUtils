#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging, logging.config, re
from logutils import log_level
from ConfigParser import ConfigParser


class ConfigParserEx(ConfigParser):

    """
    Extended ConfigParser

    Provides a Python 3.x like substitution of value references in the form ${section:option}
    and find_section(option) helper to find the (most/less specific) section for an option.

    """

    def __init__(self, *args, **kwargs):
        """
        Pass all arguments to parent constructor
        """
        ConfigParser.__init__(self, *args, **kwargs)

    def find_section(self, option, sections=None):

        """
        Search for option key in multiple sections

        Args:
            option (str): option key to search for
            sections (array): list of sections to search, use all sections if None

        Returns:
            First section where the option key was found

        Example:
            Search for the first occurence off password from the bottom of the configuration file::
            password = config.get(config.find("password", reversed(config.sections())), "password)
        """

        if sections is not None:
            search = sections
        else:
            search = self.sections()
        for section in search:
            if self.has_option(section, option):
                return section
        return None

    def get(self, section, option, raw=False, vars=None, interpolate=True):

        """
        Get interpolated option values from config file

        Provides a Python 3.x like substitution of value references in the form ${section:option}

        Args:
            section (str): config file section
            option (str): option key
            raw (bool): see ConfigParse.get() documentation
            vars (dict): see ConfigParse.get() documentation
            interpolate (bool): enable/disable interpolation
                default = True

        Returns:
            Interpolated option value

        Example:
            Sample config file::

        [options]
        path = bar

        [section]
        value = /PATH/${options:path}

        => /PATH/bar
        """

        value = ConfigParser.get(self, section, option, raw, vars)
        if interpolate:
            for reference in re.findall('\${(.+?)}', value):
                ref = reference.split(':')
                if len(ref) > 1:
                    if self.has_section(ref[0]) and self.has_option(ref[0], "ref[1]"):
                        repl = ConfigParser.get(self, ref[0], ref[1])
                        value = value.replace('${' + ref[0] + ':' + ref[1] + '}', repl, 1)
                else:
                    if self.has_option(section, ref[0]):
                        repl = ConfigParser.get(self, section, ref[0])
                        value = value.replace('${' + ref[0] + '}', repl, 1)
        return value


class Options(object):

    """
    Initialize Options object with default settings and command line options

    Generic handler for application options from different sources. Default settings may be modified by environment
    variables PREFIX_option, config file(s) entries with [options] section or command line arguments.
    Provides "Options" evaluated from
        * code: options = {}
        * config file: [options]
        * environment: PREFIX_option
        * command line: --option
    """

    def __init__(self, options={}, args=None, config=None, config_path=['./', '~/.', '/etc/'], prefix=None):

        """
        Initialize options handler.

        In general called in main() after arg_parse.

        Args:
            options (dict): application defaults
            args (object): command line options
            config (str): use configuration file
            config_path (list): search config file in path
            prefix (str): prefix for environment options

        Examples:


        """

        self._options = options                                 # default options
        self._args = args                                       # namespace from argparser
        self._opts = vars(args) if args is not None else {}     # command line args e.g. --config=...
        self._prefix = prefix                                   # environment vars PREFEX_
        self._config_path = config_path                         # config file search path

        if self._opts['config']:                                # config filename or [key] to search in opts/vars
            self._config = self._opts['config']                 # command line settings overrides default
        else: self._config = config                             # default from definition in main()

        self._config_file = None
        self._config_parser = None
        self._logger = None
        self._home = os.path.expanduser('~')
        self._script, ext = os.path.splitext(os.path.basename(sys.argv[0]))
        self._path = os.path.dirname(sys.argv[0])
        self._cwd = os.getcwd()

# region Options
    def get(self, key, default=None, type=str):
        # required to restore shadowed __builtin__.type()
        import __builtin__
        if default is not None: _type = __builtin__.type(default)
        else:_type = type
        val = self.__getitem__(key)
        return self.get_value(val, default, type)

    @staticmethod
    def get_value(val, default, _type):

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
# endregion

# region Config
    def sections(self):
        return self.config_parser.sections()

    def keys(self, section):

        # ??? contacts = dict(config.items(section))
        # ??? dictionary contains options from multiple sections ???

        # contacts = dict(config._sections[section])
        # ??? dictionary contains __len__ and __name__ metadate ???

        return {k:v for k,v in self._config_parser._sections[section].iteritems() if not k.startswith('__')}

    def value(self, section, key, default=None, type=str):

        # required to restore shadowed __builtin__.type()
        import __builtin__
        if default is not None: _type = __builtin__.type(default)
        else:_type = type
        val = self._config_parser.get(section, key)
        return self.get_value(val, default, _type)

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
                        # single filename or comma separated list of names
                        config = []
                        if self._config_path is not None:
                            #
                            for path in self._config_path:
                                path = os.path.expanduser(path)
                                config.append(os.path.join(path, self._config))
                        else:
                            config.append(self._config)
                        self._config_file = self._config
                        # if self._config_file:
                        #     self._config_file = os.path.expanduser(self._config_file)
                else:
                    # calculate config file name from path and script name
                    for path in self._config_path:
                        path = os.path.expanduser(path)
                        # config = os.path.join(path, self._script + '.cfg')
                        config = path + self._script + '.cfg'

                        if os.path.isfile(config):
                            self._config_file = config
                            break
        return self._config_file

    @property
    def config_parser(self):
        if self._config is not None:
            if self._config_parser is None:
                # if self.config_file and os.path.isfile(self.config_file):
                self._config_parser = ConfigParserEx(self._options)
                # enable case sensitive options
                self._config_parser.optionxform = str
                cfg_files = []
                for file in  map(lambda f: os.path.expanduser(f), self.config_file.split(',')):
                    if os.path.isfile(file):
                        cfg_files.append(file)
                self._config_parser.read(cfg_files)
        return self._config_parser
# endregion

    @property
    def logger(self):
        if self._logger is None:
            if self.config_parser:
                if self.__getitem__('logconfig'):
                    # logging config file specified in options
                    logcfg = os.path.expanduser(self.__getitem__('logconfig'))
                    logging.config.fileConfig(logcfg)
                elif self._config_parser.has_section('loggers'):
                    # get logger configuration from first(!) config file
                    # if a 'loggers' section is found in the configuration
                    logcfg = os.path.expanduser(self.config_file.split(',')[0])
                    logging.config.fileConfig(logcfg)
                else:
                    # default config without cfg file
                    pass
            self._logger = logging.getLogger()
            if self.__getitem__('loglevel'):
                self._logger.setLevel(log_level(self.__getitem__('loglevel')))
        return self._logger

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
