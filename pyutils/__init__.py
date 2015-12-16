import os, sys, logging

__version__ = '0.1.4'
__license__ = 'GPL2'
__author__ = 'Bernd Strebel'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .logutils import LogFileHandler, LogAdapter, ConsoleLogger
from .timeutils import strflocal

__all__ = [

    'LogAdapter',
    'LogFileHandler',
    'ConsoleLogger',
    'strflocal'
]

