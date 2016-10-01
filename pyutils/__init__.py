import os, sys, logging

__version__ = '0.4.0'
__license__ = 'GPL2'
__author__ = 'Bernd Strebel'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .logutils import LogFileHandler, LogAdapter, get_logger, log_level
from .timeutils import strflocal, localfstr
from .optutils import Options
from .unicode import utf8, string
from .dynutils import import_code

__all__ = [

    'LogAdapter',
    'LogFileHandler',
    'get_logger',
    'log_level',
    'strflocal',
    'localfstr',
    'utf8',
    'string',
    'Options',
    'import_code'
]
