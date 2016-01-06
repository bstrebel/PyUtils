import os, sys
#print sys.path

import logging
from pyutils import LogAdapter

# stream handler configuration
sh = logging.StreamHandler()
sf = logging.Formatter('%(levelname)-8s %(module)s %(message)s')
sh.setFormatter(sf)

#fh = logging.FileHandler('sync.log', encoding='utf-8')
#ff = logging.Formatter('%(asctime)s %(levelname)-8s %(module)s %(message)s')
#fh.setFormatter(ff)

# logging via LoggerAdapter
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(sh)
#root.addHandler(fh)

adapter = LogAdapter(root, {'package': 'pyutils'})

adapter.debug('Log message')

