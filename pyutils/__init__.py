import os

__version__ = '0.1.1'
__license__ = 'GPL2'
__author__ = 'Bernd Strebel'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .logutils import LogAdapter

__all__ = [

    'LogAdapter'
]
