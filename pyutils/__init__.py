import os

__version__ = '0.1.2'
__license__ = 'GPL2'
__author__ = 'Bernd Strebel'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .logutils import LogAdapter, LogFileHandler
from .timeutils import strflocal


__all__ = [

    'LogAdapter',
    'LogFileHandler',
    'strflocal'

]
